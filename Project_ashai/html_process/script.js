class SpectraProcessor {
  constructor() {
    this.metadata = this.getDefaultMetadata();
    this.files = {
      dir1: [],
      dir2: [],
      dir3: [],
    };
    this.setupEventListeners();
    this.updateMetadataDisplay();
  }

  getDefaultMetadata() {
    return {
      Product_Name: "",
      Additional_Details: "",
      Thickness: 0,
      Emissivity_back: 0.001234,
      Appearance: "",
      NFRC_id: 0,
      Substrate_filename: "",
      Wavelength: "SI Microns",
      Conductivity: 0.0,
      IR_Transmittance: 0.0123,
      Emissivity_front: 0.00123,
      Manufacturer: "AIS",
      Type: "type",
      Material: "N/A",
      Coated_Side: "front",
    };
  }

  setupEventListeners() {
    // File input listeners
    document.getElementById("dir1-files").addEventListener("change", (e) => {
      this.files.dir1 = Array.from(e.target.files).filter((f) =>
        f.name.endsWith(".asc"),
      );
      document.getElementById("dir1-count").textContent =
        `${this.files.dir1.length} .asc files selected`;
    });

    document.getElementById("dir2-files").addEventListener("change", (e) => {
      this.files.dir2 = Array.from(e.target.files).filter((f) =>
        f.name.endsWith(".asc"),
      );
      document.getElementById("dir2-count").textContent =
        `${this.files.dir2.length} .asc files selected`;
    });

    document.getElementById("dir3-files").addEventListener("change", (e) => {
      this.files.dir3 = Array.from(e.target.files).filter((f) =>
        f.name.endsWith(".asc"),
      );
      document.getElementById("dir3-count").textContent =
        `${this.files.dir3.length} .asc files selected`;
    });

    document
      .getElementById("metadata-upload")
      .addEventListener("change", async (e) => {
        await this.handleMetadataUpload(e.target.files[0]);
      });

    // Form input listeners
    const inputIds = [
      "product-name",
      "additional-details",
      "thickness",
      "emissivity-back",
      "appearance",
      "nfrc-id",
      "substrate-filename",
      "wavelength",
      "conductivity",
      "ir-transmittance",
      "emissivity-front",
      "manufacturer",
      "type",
      "material",
      "coated-side",
    ];

    inputIds.forEach((id) => {
      document.getElementById(id).addEventListener("input", (e) => {
        this.updateMetadataFromForm();
      });
    });
  }

  async handleMetadataUpload(file) {
    if (!file) return;

    try {
      const text = await this.readFileAsText(file);
      const loadedMetadata = JSON.parse(text);

      // Merge with current metadata
      this.metadata = { ...this.metadata, ...loadedMetadata };

      // Update form fields
      this.populateFormFields();
      this.updateMetadataDisplay();

      document.getElementById("metadata-info").textContent =
        `Loaded: ${file.name}`;
      document.getElementById("metadata-info").style.color = "#28a745";

      console.log("Metadata loaded successfully:", this.metadata);
    } catch (error) {
      document.getElementById("metadata-info").textContent =
        `Error: ${error.message}`;
      document.getElementById("metadata-info").style.color = "#dc3545";
      console.error("Error loading metadata:", error);
    }
  }

  readFileAsText(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = (e) => reject(new Error("Failed to read file"));
      reader.readAsText(file);
    });
  }

  populateFormFields() {
    const fields = {
      "product-name": this.metadata.Product_Name,
      "additional-details": this.metadata.Additional_Details,
      thickness: this.metadata.Thickness,
      "emissivity-back": this.metadata.Emissivity_back,
      appearance: this.metadata.Appearance,
      "nfrc-id": this.metadata.NFRC_id,
      "substrate-filename": this.metadata.Substrate_filename,
      wavelength: this.metadata.Wavelength,
      conductivity: this.metadata.Conductivity,
      "ir-transmittance": this.metadata.IR_Transmittance,
      "emissivity-front": this.metadata.Emissivity_front,
      manufacturer: this.metadata.Manufacturer,
      type: this.metadata.Type,
      material: this.metadata.Material,
      "coated-side": this.metadata.Coated_Side,
    };

    Object.entries(fields).forEach(([id, value]) => {
      const element = document.getElementById(id);
      if (element) {
        element.value = value !== undefined ? value : "";
      }
    });
  }

  updateMetadataFromForm() {
    this.metadata = {
      Product_Name: document.getElementById("product-name").value,
      Additional_Details: document.getElementById("additional-details").value,
      Thickness: parseFloat(document.getElementById("thickness").value) || 0,
      Emissivity_back:
        parseFloat(document.getElementById("emissivity-back").value) ||
        0.001234,
      Appearance: document.getElementById("appearance").value,
      NFRC_id: parseInt(document.getElementById("nfrc-id").value) || 0,
      Substrate_filename: document.getElementById("substrate-filename").value,
      Wavelength: document.getElementById("wavelength").value,
      Conductivity:
        parseFloat(document.getElementById("conductivity").value) || 0.0,
      IR_Transmittance:
        parseFloat(document.getElementById("ir-transmittance").value) || 0.0123,
      Emissivity_front:
        parseFloat(document.getElementById("emissivity-front").value) ||
        0.00123,
      Manufacturer: document.getElementById("manufacturer").value,
      Type: document.getElementById("type").value,
      Material: document.getElementById("material").value,
      Coated_Side: document.getElementById("coated-side").value,
    };

    this.updateMetadataDisplay();
  }

  updateMetadataDisplay() {
    const display = document.getElementById("metadata-content");
    display.textContent = JSON.stringify(this.metadata, null, 2);
  }

  validateInputs() {
    // Check required fields
    const required = [
      { id: "product-name", name: "Product Name" },
      { id: "thickness", name: "Thickness" },
      { id: "nfrc-id", name: "NFRC ID" },
      { id: "substrate-filename", name: "Substrate Filename" },
    ];

    for (const field of required) {
      const value = document.getElementById(field.id).value.trim();
      if (!value) {
        throw new Error(`${field.name} is required`);
      }
    }

    // Check files
    const dirs = ["dir1", "dir2", "dir3"];
    for (const dir of dirs) {
      if (this.files[dir].length === 0) {
        throw new Error(`Please select files for ${dir}`);
      }
    }

    // Check file counts match
    const counts = dirs.map((dir) => this.files[dir].length);
    const minCount = Math.min(...counts);
    const maxCount = Math.max(...counts);

    if (minCount === 0) {
      throw new Error("Each directory must contain at least one .asc file");
    }

    if (minCount !== maxCount) {
      console.warn(
        `File counts differ: ${counts.join(", ")}. Will process ${minCount} files from each.`,
      );
    }

    return minCount; // Return number of files to process
  }

  async processFiles() {
    try {
      // Show progress section
      document.getElementById("progress-section").classList.remove("hidden");
      document.getElementById("results-section").classList.remove("hidden");
      document.getElementById("results-list").innerHTML = "";

      // Validate inputs and get file count
      const fileCount = this.validateInputs();

      // Update metadata from form
      this.updateMetadataFromForm();

      const results = [];

      for (let i = 0; i < fileCount; i++) {
        // Update progress
        const progress = ((i + 1) / fileCount) * 100;
        this.updateProgress(
          progress,
          `Processing set ${i + 1} of ${fileCount}`,
        );

        try {
          // Get file set for this iteration
          const fileSet = [
            this.files.dir1[i],
            this.files.dir2[i],
            this.files.dir3[i],
          ];

          // Read and parse all three files
          const fileContents = await Promise.all(
            fileSet.map((file) => this.readFileAsText(file)),
          );

          const parsedData = fileContents.map((content) =>
            this.parseASCFile(content),
          );

          // Generate output filename
          const outputFilename = this.generateOutputFilename(i);

          // Create merged content
          const mergedContent = this.createMergedFile(
            parsedData,
            outputFilename,
          );

          // Create download link for the file
          this.createDownloadLink(outputFilename, mergedContent);

          // Add to results
          results.push({
            filename: outputFilename,
            status: "Success",
            files: fileSet.map((f) => f.name),
          });

          // Display result
          this.addResult(outputFilename, "Success");
        } catch (error) {
          results.push({
            index: i,
            status: "Error",
            error: error.message,
          });
          this.addResult(`File set ${i + 1}`, `Error: ${error.message}`);
        }
      }

      this.updateProgress(100, "Processing complete!");

      // Save results summary
      this.saveResultsSummary(results);
    } catch (error) {
      this.showError(error.message);
    }
  }

  parseASCFile(content) {
    const lines = content.split("\n");
    let inDataSection = false;
    const data = [];

    for (const line of lines) {
      const trimmedLine = line.trim();

      if (trimmedLine.startsWith("#DATA")) {
        inDataSection = true;
        continue;
      }

      if (inDataSection && trimmedLine && !trimmedLine.startsWith("#")) {
        const parts = trimmedLine.split(/\s+/).filter((p) => p.length > 0);

        if (parts.length >= 2) {
          const wavelength = parseFloat(parts[0]);
          const measurement = parseFloat(parts[1]);

          if (!isNaN(wavelength) && !isNaN(measurement)) {
            data.push({
              wavelength: wavelength,
              measurement: measurement,
            });
          }
        }
      }
    }

    return data;
  }

  generateOutputFilename(index) {
    const nfrcId = this.metadata.NFRC_id || "unknown";
    const productName = (this.metadata.Product_Name || "product").split("_")[0];
    const thickness = this.metadata.Thickness || 0;
    const additional = this.metadata.Additional_Details || "";

    // Clean special characters from additional details
    const cleanAdditional = additional
      .replace(/[^a-zA-Z0-9\s-]/g, "")
      .trim()
      .replace(/\s+/g, "_");

    let filename = `${nfrcId}_${productName}_${thickness}mm`;

    if (cleanAdditional) {
      filename += `_${cleanAdditional}`;
    } else if (fileCount > 1) {
      filename += `_batch${index + 1}`;
    }

    return filename + ".txt";
  }

  createMergedFile(parsedData, filename) {
    const header = this.createHeader(filename);
    const dataLines = this.mergeDataLines(parsedData);

    return header + "\n" + dataLines.join("\n");
  }

  createHeader(filename) {
    const checksum = (
      (this.metadata.Emissivity_front || 0) +
      (this.metadata.Emissivity_back || 0)
    ).toFixed(6);

    const coatingName =
      `${this.metadata.Product_Name || ""}_${this.metadata.Thickness || 0}mm_${this.metadata.Additional_Details || ""}`
        .replace(/\s+/g, "_")
        .trim("_");

    return `{ Units Wavelength Units } ${this.metadata.Wavelength || "SI Microns"}
{ Thickness } ${this.metadata.Thickness || 0}
{ Conductivity } ${this.metadata.Conductivity || 0.0}
{ IR Transmittance } TIR=${this.metadata.IR_Transmittance || 0.0123}
{ Emissivity front back } Emis= ${this.metadata.Emissivity_front || 0.00123} ${this.metadata.Emissivity_back || 0.001234}
{ Ef_Source: Text Files }
{ Eb_Source: Text Files }
{ IGDB_Checksum: ${checksum} }
{ Product Name: ${filename} }
{ Manufacturer: ${this.metadata.Manufacturer || "AIS"} }
{ NFRC ID: ${this.metadata.NFRC_id || 0} }
{ Type: ${this.metadata.Type || "type"} }
{ Material: ${this.metadata.Material || "N/A"} }
{ Coating Name: ${coatingName} }
{ Coated Side: ${this.metadata.Coated_Side || "front"} }
{ Substrate Filename: ${this.metadata.Substrate_filename || ""} }
{ Appearance: ${this.metadata.Appearance || ""} }
{ Acceptance: # }
{ Uses: Glass }
{ Availability: X }
{ Structure: }`;
  }

  mergeDataLines(parsedData) {
    // Use the first file as reference for wavelength points
    const referenceData = parsedData[0];
    const dataLines = [];

    for (let i = 0; i < referenceData.length; i++) {
      const values = [];

      // First column: wavelength from first file divided by 1000
      values.push((referenceData[i].wavelength / 1000).toFixed(6));

      // Next three columns: measurements from each file divided by 100
      for (let j = 0; j < Math.min(3, parsedData.length); j++) {
        if (parsedData[j] && parsedData[j][i]) {
          values.push((parsedData[j][i].measurement / 100).toFixed(6));
        } else {
          values.push("0.000000");
        }
      }

      dataLines.push(values.join(" "));
    }

    return dataLines;
  }

  updateProgress(percentage, message) {
    document.getElementById("progress-fill").style.width = `${percentage}%`;
    document.getElementById("progress-text").textContent =
      `${Math.round(percentage)}%`;
    document.getElementById("status-message").textContent = message;
  }

  addResult(filename, status) {
    const resultsList = document.getElementById("results-list");
    const resultItem = document.createElement("div");
    resultItem.className = "result-item";
    resultItem.innerHTML = `
            <div><strong>${filename}</strong></div>
            <div>Status: <span class="status-${status.toLowerCase()}">${status}</span></div>
        `;
    resultsList.appendChild(resultItem);
  }

  createDownloadLink(filename, content) {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.textContent = `Download ${filename}`;
    link.style.display = "block";
    link.style.margin = "5px 0";

    const resultsList = document.getElementById("results-list");
    const container = document.createElement("div");
    container.className = "download-link";
    container.appendChild(link);
    resultsList.appendChild(container);

    // Auto-click after a short delay
    setTimeout(() => {
      link.click();
      URL.revokeObjectURL(url);
    }, 100);
  }

  saveResultsSummary(results) {
    const summary = {
      metadata: this.metadata,
      results: results,
      timestamp: new Date().toISOString(),
      totalProcessed: results.filter((r) => r.status === "Success").length,
      totalErrors: results.filter((r) => r.status === "Error").length,
    };

    const blob = new Blob([JSON.stringify(summary, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `processing_summary_${new Date().getTime()}.json`;
    link.textContent = "Download Processing Summary";
    link.style.display = "block";
    link.style.marginTop = "20px";
    link.style.padding = "10px";
    link.style.backgroundColor = "#28a745";
    link.style.color = "white";
    link.style.textAlign = "center";
    link.style.borderRadius = "5px";
    link.style.textDecoration = "none";

    document.getElementById("results-section").appendChild(link);

    setTimeout(() => {
      link.click();
      URL.revokeObjectURL(url);
    }, 500);
  }

  showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.style.backgroundColor = "#f8d7da";
    errorDiv.style.color = "#721c24";
    errorDiv.style.padding = "15px";
    errorDiv.style.margin = "10px 0";
    errorDiv.style.borderRadius = "5px";
    errorDiv.style.border = "1px solid #f5c6cb";
    errorDiv.innerHTML = `<strong>Error:</strong> ${message}`;

    document.getElementById("results-section").prepend(errorDiv);

    // Remove after 5 seconds
    setTimeout(() => {
      errorDiv.remove();
    }, 5000);
  }

  saveMetadata() {
    this.updateMetadataFromForm();
    const blob = new Blob([JSON.stringify(this.metadata, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `metadata_${new Date().getTime()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  loadDefaultMetadata() {
    this.metadata = this.getDefaultMetadata();
    this.populateFormFields();
    this.updateMetadataDisplay();
    alert("Default metadata loaded!");
  }

  resetForm() {
    if (
      confirm(
        "Are you sure you want to reset the form? All unsaved data will be lost.",
      )
    ) {
      // Reset form fields
      document.querySelector(".form-container").reset();

      // Reset file arrays
      this.files = { dir1: [], dir2: [], dir3: [] };

      // Reset file counters
      ["dir1", "dir2", "dir3"].forEach((dir) => {
        document.getElementById(`${dir}-count`).textContent =
          "0 files selected";
      });

      // Reset metadata info
      document.getElementById("metadata-info").textContent = "No file selected";
      document.getElementById("metadata-info").style.color = "";

      // Reset metadata
      this.metadata = this.getDefaultMetadata();
      this.updateMetadataDisplay();

      // Hide results
      document.getElementById("progress-section").classList.add("hidden");
      document.getElementById("results-section").classList.add("hidden");
      document.getElementById("results-list").innerHTML = "";

      // Clear file inputs
      document.getElementById("dir1-files").value = "";
      document.getElementById("dir2-files").value = "";
      document.getElementById("dir3-files").value = "";
      document.getElementById("metadata-upload").value = "";
    }
  }
}

// Initialize the application
const processor = new SpectraProcessor();

// Global functions for HTML onclick handlers
function processFiles() {
  processor.processFiles();
}

function saveMetadata() {
  processor.saveMetadata();
}

function loadDefaultMetadata() {
  processor.loadDefaultMetadata();
}

function resetForm() {
  processor.resetForm();
}

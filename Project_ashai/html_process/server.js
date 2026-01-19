const express = require("express");
const multer = require("multer");
const fs = require("fs").promises;
const path = require("path");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configure storage
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/");
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, uniqueSuffix + "-" + file.originalname);
  },
});

const upload = multer({
  storage: storage,
  fileFilter: function (req, file, cb) {
    if (file.fieldname === "files") {
      // Allow only .asc files for spectra data
      if (file.originalname.endsWith(".asc")) {
        cb(null, true);
      } else {
        cb(new Error("Only .asc files are allowed for spectra data"));
      }
    } else if (file.fieldname === "metadata") {
      // Allow only .json files for metadata
      if (file.originalname.endsWith(".json")) {
        cb(null, true);
      } else {
        cb(new Error("Only .json files are allowed for metadata"));
      }
    } else {
      cb(null, true);
    }
  },
});

// Ensure uploads directory exists
const ensureUploadsDir = async () => {
  try {
    await fs.mkdir("uploads", { recursive: true });
  } catch (error) {
    console.error("Error creating uploads directory:", error);
  }
};

// API Endpoints

// Health check
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// Upload and process metadata
app.post(
  "/api/upload-metadata",
  upload.single("metadata"),
  async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ error: "No metadata file uploaded" });
      }

      const filePath = req.file.path;
      const content = await fs.readFile(filePath, "utf8");
      const metadata = JSON.parse(content);

      // Clean up the uploaded file
      await fs.unlink(filePath);

      res.json({
        success: true,
        metadata: metadata,
        message: "Metadata uploaded successfully",
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  },
);

// Process ASC files
app.post("/api/process", upload.array("files"), async (req, res) => {
  try {
    await ensureUploadsDir();

    const { metadata, outputDir } = req.body;
    const files = req.files;

    if (!files || files.length === 0) {
      return res.status(400).json({ error: "No files uploaded" });
    }

    if (!metadata) {
      return res.status(400).json({ error: "Metadata is required" });
    }

    // Parse metadata
    let parsedMetadata;
    try {
      parsedMetadata =
        typeof metadata === "string" ? JSON.parse(metadata) : metadata;
    } catch (error) {
      return res.status(400).json({ error: "Invalid metadata format" });
    }

    // Group files by directory indicator (first part of filename)
    const fileGroups = {};
    files.forEach((file) => {
      const filename = file.originalname;
      const dirIndicator = filename.split("_")[0] || "unknown";

      if (!fileGroups[dirIndicator]) {
        fileGroups[dirIndicator] = [];
      }

      // Store file info
      fileGroups[dirIndicator].push({
        path: file.path,
        filename: filename,
        originalname: file.originalname,
      });
    });

    const groupKeys = Object.keys(fileGroups);
    if (groupKeys.length < 3) {
      return res.status(400).json({
        error: "Files must be from at least 3 different directories/groups",
      });
    }

    // Process files
    const results = [];
    const firstGroup = fileGroups[groupKeys[0]];
    const fileCount = Math.min(
      ...Object.values(fileGroups).map((g) => g.length),
    );

    for (let i = 0; i < fileCount; i++) {
      try {
        // Get one file from each group
        const fileSet = groupKeys.map((key) => fileGroups[key][i]);

        // Read and parse all files
        const parsedData = await Promise.all(
          fileSet.map((file) => parseASCFile(file.path)),
        );

        // Generate output filename
        const outputFilename = generateOutputFilename(parsedMetadata, i);
        const mergedContent = createMergedFile(
          parsedData,
          parsedMetadata,
          outputFilename,
        );

        // Create output directory if it doesn't exist
        const outputPath = path.join(outputDir || "output", outputFilename);
        await fs.mkdir(path.dirname(outputPath), { recursive: true });

        // Write output file
        await fs.writeFile(outputPath, mergedContent);

        results.push({
          index: i,
          filename: outputFilename,
          path: outputPath,
          status: "success",
          inputFiles: fileSet.map((f) => f.originalname),
        });
      } catch (error) {
        results.push({
          index: i,
          status: "error",
          error: error.message,
        });
      }
    }

    // Clean up uploaded files
    for (const group of Object.values(fileGroups)) {
      for (const file of group) {
        try {
          await fs.unlink(file.path);
        } catch (error) {
          console.warn(`Could not delete file ${file.path}:`, error.message);
        }
      }
    }

    res.json({
      success: true,
      totalProcessed: fileCount,
      results: results,
      summary: {
        successful: results.filter((r) => r.status === "success").length,
        failed: results.filter((r) => r.status === "error").length,
      },
    });
  } catch (error) {
    console.error("Processing error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Helper function to parse ASC file
async function parseASCFile(filePath) {
  const content = await fs.readFile(filePath, "utf8");
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
          data.push({ wavelength, measurement });
        }
      }
    }
  }

  if (data.length === 0) {
    throw new Error("No valid data found in file");
  }

  return data;
}

// Helper function to generate output filename
function generateOutputFilename(metadata, index) {
  const nfrcId = metadata.NFRC_id || "unknown";
  const productName = (metadata.Product_Name || "product").split("_")[0];
  const thickness = metadata.Thickness || 0;
  const additional = metadata.Additional_Details || "";

  // Clean additional details for filename
  const cleanAdditional = additional
    .replace(/[^a-zA-Z0-9\s-]/g, "")
    .trim()
    .replace(/\s+/g, "_");

  let filename = `${nfrcId}_${productName}_${thickness}mm`;

  if (cleanAdditional) {
    filename += `_${cleanAdditional}`;
  } else {
    filename += `_batch${index + 1}`;
  }

  return filename + ".txt";
}

// Helper function to create merged file
function createMergedFile(parsedData, metadata, filename) {
  const header = createHeader(metadata, filename);
  const dataLines = mergeDataLines(parsedData);

  return header + "\n" + dataLines.join("\n");
}

function createHeader(metadata, filename) {
  const checksum = (
    (metadata.Emissivity_front || 0) + (metadata.Emissivity_back || 0)
  ).toFixed(6);

  const coatingName =
    `${metadata.Product_Name || ""}_${metadata.Thickness || 0}mm_${metadata.Additional_Details || ""}`
      .replace(/\s+/g, "_")
      .trim("_");

  return `{ Units Wavelength Units } ${metadata.Wavelength || "SI Microns"}
{ Thickness } ${metadata.Thickness || 0}
{ Conductivity } ${metadata.Conductivity || 0.0}
{ IR Transmittance } TIR=${metadata.IR_Transmittance || 0.0123}
{ Emissivity front back } Emis= ${metadata.Emissivity_front || 0.00123} ${metadata.Emissivity_back || 0.001234}
{ Ef_Source: Text Files }
{ Eb_Source: Text Files }
{ IGDB_Checksum: ${checksum} }
{ Product Name: ${filename} }
{ Manufacturer: ${metadata.Manufacturer || "AIS"} }
{ NFRC ID: ${metadata.NFRC_id || 0} }
{ Type: ${metadata.Type || "type"} }
{ Material: ${metadata.Material || "N/A"} }
{ Coating Name: ${coatingName} }
{ Coated Side: ${metadata.Coated_Side || "front"} }
{ Substrate Filename: ${metadata.Substrate_filename || ""} }
{ Appearance: ${metadata.Appearance || ""} }
{ Acceptance: # }
{ Uses: Glass }
{ Availability: X }
{ Structure: }`;
}

function mergeDataLines(parsedData) {
  const referenceData = parsedData[0];
  const dataLines = [];

  for (let i = 0; i < referenceData.length; i++) {
    const values = [];

    // First column: wavelength from first file divided by 1000
    values.push((referenceData[i].wavelength / 1000).toFixed(6));

    // Next columns: measurements from each file divided by 100
    for (let j = 0; j < parsedData.length; j++) {
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

// Download endpoint
app.get("/api/download/:filename", async (req, res) => {
  try {
    const filename = req.params.filename;
    const filePath = path.join("output", filename);

    if (
      !(await fs
        .access(filePath)
        .then(() => true)
        .catch(() => false))
    ) {
      return res.status(404).json({ error: "File not found" });
    }

    res.download(filePath);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Serve static files
app.use(express.static("public"));

// Start server
app.listen(PORT, async () => {
  await ensureUploadsDir();
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Uploads directory: ${path.join(process.cwd(), "uploads")}`);
});

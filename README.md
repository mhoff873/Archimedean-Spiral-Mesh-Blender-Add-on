# Archimedean Spiral Mesh Add-on for Blender

This Blender add-on allows users to create a 3D Archimedean spiral mesh directly in the Blender viewport. It was designed to simulate coiling a tube in a spiral pattern.

![Alt text](/spiral_1.png?raw=true "Spiral")
## Features

- Create Archimedean spiral meshes with adjustable parameters:
  - Distance from the center to the start of the spiral.
  - Distance between each ring of the spiral.
  - Total length of the spiral.
  - Number of vertices around the tube for smoothness.
  - Radius of the spiral's cross-section.
  - Smoothness along the length of the spiral

## Installation

To install this add-on in Blender:

1. Download the `.py` file for the add-on.
2. Open Blender and go to `Edit` > `Preferences`.
3. In the Preferences window, go to the `Add-ons` section.
4. Click on `Install...` and navigate to the downloaded `.py` file.
5. Select the file and click `Install Add-on`.
6. Enable the add-on by ticking the checkbox next to its name.

## Usage

Once installed and enabled, you can find the Archimedean Spiral mesh under the `Add` > `Mesh`> `Mason's Meshes` menu in the 3D Viewport:

1. Navigate to `Add` > `Mesh` > `Mason's Meshes` > `Archimedean Spiral Mesh`.
2. Adjust the parameters in the operator panel to customize your spiral.

## Parameters

- **Spiral Start**: Starting distance of the spiral from the center point.
- **Spiral Gap**: The space between each ring of the spiral.
- **Spiral Length**: Total length of the spiral.
- **Ring Radius**: The radius of the tubular spiral.
- **Ring Vertices**: Number of vertices around each tube ring for defining the tube's roundness.
- **Ring Density**: Density of the rings along the length of the spiral.

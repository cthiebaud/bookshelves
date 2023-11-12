// Function to convert RGB to LAB
function rgbToLab(rgb) {
    const r = rgb[0] / 255;
    const g = rgb[1] / 255;
    const b = rgb[2] / 255;

    // Convert RGB to XYZ
    let x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375;
    let y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750;
    let z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041;

    // Normalize XYZ to D65 illuminant
    x /= 95.047;
    y /= 100.000;
    z /= 108.883;

    // Convert XYZ to LAB
    x = (x > 0.008856) ? Math.cbrt(x) : (903.3 * x + 16) / 116;
    y = (y > 0.008856) ? Math.cbrt(y) : (903.3 * y + 16) / 116;
    z = (z > 0.008856) ? Math.cbrt(z) : (903.3 * z + 16) / 116;

    const L = Math.max(0, 116 * y - 16);
    const a = (x - y) * 500;
    const b2 = (y - z) * 200;

    return [L, a, b2];
}

// Function to calculate CIEDE2000 color difference between two LAB color values
// Function to calculate CIEDE2000 color difference between two LAB color values
function ciede2000_color_difference(Lab1, Lab2) {
    const L1 = Lab1[0];
    const a1 = Lab1[1];
    const b1 = Lab1[2];
    const L2 = Lab2[0];
    const a2 = Lab2[1];
    const b2 = Lab2[2];

    // Constants for CIEDE2000 calculation
    const KL = 1;
    const KC = 1;
    const KH = 1;

    function delta_L(L1, L2) {
        return L2 - L1;
    }

    function delta_C(C1, C2) {
        return C2 - C1;
    }

    function delta_H(H1, H2, C1, C2) {
        let delta_h = H2 - H1;
        delta_h = (Math.abs(delta_h) <= 180) ? delta_h : (delta_h > 0) ? delta_h - 360 : delta_h + 360;
        return 2 * Math.sqrt(C1 * C2) * Math.sin(delta_h / 2);
    }

    function mean(a, b) {
        return (a + b) / 2;
    }

    function mean_L(L1, L2) {
        return mean(L1, L2);
    }

    function mean_C(C1, C2) {
        return mean(C1, C2);
    }

    function mean_H(H1, H2, C1, C2) {
        return mean(H1, H2) + (Math.abs(H1 - H2) > 180 ? 180 : 0);
    }

    function C_prime(C, L) {
        return Math.sqrt(C * C + KL * (L - 50) * (L - 50));
    }

    function H_prime(H, C, L) {
        return (180 / Math.PI) * Math.atan2(C * Math.sin((Math.PI / 180) * H), C * Math.cos((Math.PI / 180) * H));
    }

    const C1 = Math.sqrt(a1 * a1 + b1 * b1);
    const C2 = Math.sqrt(a2 * a2 + b2 * b2);

    const L1L2 = mean_L(L1, L2);
    const C1C2 = mean_C(C1, C2);
    const H1H2 = mean_H(H_prime(a1, C1, L1), H_prime(a2, C2, L2), C1, C2);

    const delta_L_ = delta_L(L1, L2);
    const delta_C_ = delta_C(C1, C2);
    const delta_H_ = delta_H(H1, H2, C1, C2);

    const SL = 1 + (0.015 * (L1L2 - 50) * (L1L2 - 50)) / Math.sqrt(20 + (L1L2 - 50) * (L1L2 - 50));
    const SC = 1 + 0.045 * C1C2;
    const SH = 1 + 0.015 * C1C2 * (1 - Math.cos((Math.PI / 180) * (H1H2 - 160)));

    const delta_theta = 30 * Math.exp(-((H1H2 - 275) / 25) * ((H1H2 - 275) / 25));
    const RC = 2 * Math.sqrt(Math.pow(C1C2, 7) / (Math.pow(C1C2, 7) + Math.pow(25, 7)));
    const RT = -RC * Math.sin((2 * (Math.PI / 180)) * delta_theta);

    return Math.sqrt((delta_L_ / (KL * SL)) * (delta_L_ / (KL * SL)) + (delta_C_ / (KC * SC)) * (delta_C_ / (KC * SC)) + (delta_H_ / (KH * SH)) * (delta_H_ / (KH * SH)) + RT * (delta_C_ / (KC * SC)) * (delta_H_ / (KH * SH)))
}

// Your color palette as an array of RGB color values
const palette = [
    [255, 0, 0],  // Red
    [0, 255, 0],  // Green
    [0, 0, 255],  // Blue
    // Add more RGB colors
];

// Convert RGB colors to LAB colors
const labPalette = palette.map(rgbToLab);

// Calculate the color differences between all pairs of colors
let totalDifference = 0;
let pairCount = 0;

for (let i = 0; i < labPalette.length; i++) {
    for (let j = i + 1; j < labPalette.length; j++) {
        const diff = ciede2000_color_difference(labPalette[i], labPalette[j]);
        totalDifference += diff;
        pairCount++;
    }
}

// Calculate the average color difference as the diversity indicator
const diversityIndicator = totalDifference / pairCount;

console.log('Diversity Indicator:', diversityIndicator);

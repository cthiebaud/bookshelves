// planeOperations.js
function extractPlaneInfo(A, B, C, D) {
    // Extract the normal vector
    const planeCoefficients = {A:A, B:B, C:C, D:D}
    const planeNormal = [A, B, C];

    // Find a point on the plane
    let planePoint;
    if (A !== 0) {
        planePoint = [-D / A, 0, 0];
    } else if (B !== 0) {
        planePoint = [0, -D / B, 0];
    } else if (C !== 0) {
        planePoint = [0, 0, -D / C];
    } else {
        // Handle the case where the coefficients are invalid
        console.error("Invalid coefficients. Plane is not well-defined.");
        return null;
    }

    return { planeNormal, planePoint, planeCoefficients };
}

export { extractPlaneInfo }
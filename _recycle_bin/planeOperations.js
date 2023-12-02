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

function orthographicProjectionOnLine(pointA, pointB, pointC) {
    // Calculate the direction vector AB
    const vectorAB = { x: pointB.x - pointA.x, y: pointB.y - pointA.y };

    // Calculate the vector AC
    const vectorAC = { x: pointC.x - pointA.x, y: pointC.y - pointA.y };

    // Calculate the dot product AC dot AB
    const dotProductACAB = vectorAC.x * vectorAB.x + vectorAC.y * vectorAB.y;

    // Calculate the squared magnitude of AB
    const magnitudeSquaredAB = vectorAB.x ** 2 + vectorAB.y ** 2;

    // Calculate the projection of AC onto AB
    const projectionACAB = {
        x: (dotProductACAB / magnitudeSquaredAB) * vectorAB.x,
        y: (dotProductACAB / magnitudeSquaredAB) * vectorAB.y
    };

    // Calculate the coordinates of the orthographic projection
    const projectionPoint = { x: pointA.x + projectionACAB.x, y: pointA.y + projectionACAB.y };

    return projectionPoint;
}

export { extractPlaneInfo, orthographicProjectionOnLine }
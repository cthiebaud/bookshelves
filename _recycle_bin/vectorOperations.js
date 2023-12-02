// vectorOperations.js

function orthographicProjection(point, planeNormal, planePoint) {
    // Convert inputs to arrays for vector operations
    const pointArray = [...point];
    const planeNormalArray = [...planeNormal];
    const planePointArray = [...planePoint];

    // Calculate the projection
    const projection = pointArray.map((coord, i) =>
        coord - (dotProduct(planeNormalArray, vectorSubtraction(pointArray, planePointArray)) / magnitudeSquared(planeNormalArray)) * planeNormalArray[i]
    );

    return projection;
}

function orthographicProjectionSet(points, planeNormal, planePoint) {
    const pointArray = points.x.map((x, i) => [x, points.y[i], points.z[i]]);
    // Calculate the projection for each point in the set
    const projections = pointArray.map(point =>
        orthographicProjection(point, planeNormal, planePoint)
    );

    return projections;
}

export function dotProduct(vector1, vector2) {
    return vector1.reduce((sum, value, i) => sum + value * vector2[i], 0);
}

export function vectorSubtraction(vector1, vector2) {
    return vector1.map((coord, i) => coord - vector2[i]);
}

export function magnitudeSquared(vector) {
    return vector.reduce((sum, value) => sum + value ** 2, 0);
}

export { orthographicProjection, orthographicProjectionSet }
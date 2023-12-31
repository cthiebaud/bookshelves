function extractPlaneInfo(A, B, C, D) {
    // extract the normal vector
    const planeCoefficients = {A:A, B:B, C:C, D:D}
    const planeNormal = [A, B, C]

    // find a point on the plane
    let planePoint
    if (A !== 0) {
        planePoint = [-D / A, 0, 0]
    } else if (B !== 0) {
        planePoint = [0, -D / B, 0]
    } else if (C !== 0) {
        planePoint = [0, 0, -D / C]
    } else {
        // handle the case where the coefficients are invalid
        console.error("Invalid coefficients. Plane is not well-defined.")
        return null
    }

    return { planeNormal, planePoint, planeCoefficients }
}

function orthographicProjection(point, planeNormal, planePoint) {
    // convert inputs to arrays for vector operations
    const pointArray = [...point]
    const planeNormalArray = [...planeNormal]
    const planePointArray = [...planePoint]

    // calculate the projection
    const projection = pointArray.map((coord, i) =>
        coord - (dotProduct(planeNormalArray, vectorSubtraction(pointArray, planePointArray)) / magnitudeSquared(planeNormalArray)) * planeNormalArray[i]
    )

    return projection
}

function orthographicProjectionSet(points, planeNormal, planePoint) {
    const pointArray = points.x.map((x, i) => [x, points.y[i], points.z[i]])
    // calculate the projection for each point in the set
    const projections = pointArray.map(point =>
        orthographicProjection(point, planeNormal, planePoint)
    )

    return projections
}

export function dotProduct(vector1, vector2) {
    return vector1.reduce((sum, value, i) => sum + value * vector2[i], 0)
}

export function vectorSubtraction(vector1, vector2) {
    return vector1.map((coord, i) => coord - vector2[i])
}

export function magnitudeSquared(vector) {
    return vector.reduce((sum, value) => sum + value ** 2, 0)
}

export { extractPlaneInfo, orthographicProjection, orthographicProjectionSet }
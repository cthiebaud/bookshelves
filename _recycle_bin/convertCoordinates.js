function convertCoordinates2DTo3D(X, Y, planeNormal, pointOnPlane) {
    // Normalize the plane normal vector
    const normal = normalizeVector(planeNormal);

    // Calculate the displacement vector from the point on the plane to the origin
    const displacementVector = {
        x: pointOnPlane.x,
        y: pointOnPlane.y,
        z: pointOnPlane.z,
    };

    // Calculate the projection of the displacement vector onto the plane normal
    const dotProduct = dotProduct3D(displacementVector, normal);
    const scaledNormal = scaleVector(normal, dotProduct);

    // Calculate the position in 3D space
    const position = {
        x: X,
        y: Y,
        z: 0,
    };

    // Calculate the final 3D coordinates
    const result = addVectors(position, scaledNormal);

    return result;
}

function convertCoordinates3DTo2D(X, Y, Z, planeNormal, pointOnPlane) {
    // Normalize the plane normal vector
    const normal = normalizeVector(planeNormal);

    // Calculate the right and up vectors, which are orthogonal to the plane normal
    const right = normalizeVector({
        x: 1 - Math.abs(normal.x),
        y: normal.y,
        z: normal.z,
    });

    const up = crossProduct3D(normal, right);

    // Calculate the position vector from the point on the plane to the origin
    const positionVector = {
        x: X - pointOnPlane.x,
        y: Y - pointOnPlane.y,
        z: Z - pointOnPlane.z,
    };

    // Calculate the dot products
    const dotProductPositionRight = dotProduct3D(positionVector, right);
    const dotProductPositionUp = dotProduct3D(positionVector, up);
    const dotProductPositionNormal = dotProduct3D(positionVector, normal);

    // Calculate the 2D coordinates
    const X2D = dotProductPositionRight;
    const Y2D = dotProductPositionUp;

    return { X: X2D, Y: Y2D };
}

function __convertCoordinates2DTo3D(X, Y, planeNormal, pointOnPlane) {
    // Normalize the plane normal vector
    const normal = normalizeVector(planeNormal);

    // Calculate the displacement vector from the point on the plane to the origin
    const displacementVector = {
        x: pointOnPlane.x,
        y: pointOnPlane.y,
        z: pointOnPlane.z,
    };

    // Calculate the projection of the displacement vector onto the plane normal
    const dotProduct = dotProduct3D(displacementVector, normal);
    const scaledNormal = scaleVector(normal, dotProduct);

    // Calculate the position in 3D space
    const position = {
        x: X,
        y: Y,
        z: 0,
    };

    // Calculate the final 3D coordinates
    const result = addVectors(position, scaledNormal);

    return result;
}

// Helper function to normalize a 3D vector
function normalizeVector(vector) {
    const length = Math.sqrt(vector.x ** 2 + vector.y ** 2 + vector.z ** 2);
    return {
        x: vector.x / length,
        y: vector.y / length,
        z: vector.z / length,
    };
}

// Helper function to calculate the dot product of two 3D vectors
function dotProduct3D(a, b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

// Helper function to scale a 3D vector by a scalar
function scaleVector(vector, scalar) {
    return {
        x: vector.x * scalar,
        y: vector.y * scalar,
        z: vector.z * scalar,
    };
}

// Helper function to add two 3D vectors
function addVectors(a, b) {
    return {
        x: a.x + b.x,
        y: a.y + b.y,
        z: a.z + b.z,
    };
}

//// // Example usage
//// const point2D = { X: 1, Y: 2 };
//// const planeNormal = { x: 0, y: 0, z: 1 }; // Assuming the plane is parallel to the xy-plane
//// const pointOnPlane = { x: 0, y: 0, z: 5 }; // A point on the plane
//// 
//// const point3D = convertCoordinates2DTo3D(point2D.X, point2D.Y, planeNormal, pointOnPlane);
//// console.log(point3D);

function _convertCoordinates2DTo3D(X, Y, planeNormal, pointOnPlane) {
    // Normalize the plane normal vector
    const normal = normalizeVector(planeNormal);

    // Calculate the displacement vector from the point on the plane to the origin
    const displacementVector = {
        x: pointOnPlane.x,
        y: pointOnPlane.y,
        z: pointOnPlane.z,
    };

    // Calculate the projection of the displacement vector onto the plane normal
    const dotProduct = dotProduct3D(displacementVector, normal);
    const scaledNormal = scaleVector(normal, dotProduct);

    // Calculate the right and up vectors, which are orthogonal to the plane normal
    const right = normalizeVector({
        x: 1 - Math.abs(normal.x),
        y: normal.y,
        z: normal.z,
    });

    const up = crossProduct3D(normal, right);

    // Calculate the position in 3D space
    const position = {
        x: X,
        y: Y,
        z: 0,
    };

    // Calculate the final 3D coordinates
    const result = addVectors(position, scaledNormal);
    result.x += right.x * X;
    result.y += right.y * X;
    result.z += right.z * X;

    result.x += up.x * Y;
    result.y += up.y * Y;
    result.z += up.z * Y;

    return result;
}

// Helper function to calculate the cross product of two 3D vectors
function crossProduct3D(a, b) {
    return {
        x: a.y * b.z - a.z * b.y,
        y: a.z * b.x - a.x * b.z,
        z: a.x * b.y - a.y * b.x,
    };
}

//// / Other helper functions are the same as in the previous example
//// 
//// / Example usage
//// onst point2D = { X: 1, Y: 2 };
//// onst planeNormal = { x: 1, y: 2, z: 3 }; // Example normal vector
//// onst pointOnPlane = { x: 0, y: 0, z: 5 }; // A point on the plane
//// 
//// onst point3D = convertCoordinates2DTo3D(point2D.X, point2D.Y, planeNormal, pointOnPlane);
//// onsole.log(point3D);

function __convertCoordinates3DTo2D(X, Y, Z, planeNormal, pointOnPlane) {
    // Normalize the plane normal vector
    const normal = normalizeVector(planeNormal);

    // Calculate the right and up vectors, which are orthogonal to the plane normal
    const right = normalizeVector({
        x: 1 - Math.abs(normal.x),
        y: normal.y,
        z: normal.z,
    });

    const up = crossProduct3D(normal, right);

    // Calculate the position vector from the point on the plane to the origin
    const positionVector = {
        x: X - pointOnPlane.x,
        y: Y - pointOnPlane.y,
        z: Z - pointOnPlane.z,
    };

    // Calculate the dot products
    const dotProductPositionRight = dotProduct3D(positionVector, right);
    const dotProductPositionUp = dotProduct3D(positionVector, up);
    const dotProductPositionNormal = dotProduct3D(positionVector, normal);

    // Calculate the 2D coordinates
    const X2D = dotProductPositionRight;
    const Y2D = dotProductPositionUp;

    return { X: X2D, Y: Y2D };
}

export {convertCoordinates2DTo3D, convertCoordinates3DTo2D}
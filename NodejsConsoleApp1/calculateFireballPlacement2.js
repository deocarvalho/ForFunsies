function printGrid(grid) {
    for (const row of grid) {
        console.log(row.join(' '));
    }
}

function distanceSquared(x1, y1, x2, y2) {
    return (x1 - x2) ** 2 + (y1 - y2) ** 2;
}

function calculateFireballImpactArea(centerX, centerY, radiusSquared, gridSize) {
    const affectedSquares = [];
    const radius = Math.floor(Math.sqrt(radiusSquared));

    // Ensure we round and clip to integer bounds within the grid limits
    const lowerBoundX = Math.max(0, centerX - radius);
    const upperBoundX = Math.min(gridSize, centerX + radius + 1);
    const lowerBoundY = Math.max(0, centerY - radius);
    const upperBoundY = Math.min(gridSize, centerY + radius + 1);

    for (let x = lowerBoundX; x < upperBoundX; x++) {
        for (let y = lowerBoundY; y < upperBoundY; y++) {
            if ((centerX - centerY) ** 2 + (x - y + 1.0) ** 2 <= radiusSquared) {
                affectedSquares.push([x, y]);
            }
        }
    }
    return affectedSquares;
}

const enemyMark = '?';
const burntEnemyMark = '?';
const fireballBlastMark = '*';
const spaceMark = ' ';

function calculateFireballPlacement(enemies, gridSize = 24) {
    const radius = 4.0;
    const radiusSquared = radius ** 2;
    const enemyLocations = new Set(enemies.map(enemy => enemy.toString()));

    let bestCount = 0;
    let bestCenter = [0, 0];

    const grid = Array(gridSize).fill().map(() => Array(gridSize).fill(spaceMark));

    for (const [ex, ey] of enemies) {
        grid[ey][ex] = enemyMark;
    }

    const impactDict = new Map();
    for (let cx = 0; cx < gridSize; cx++) {
        for (let cy = 0; cy < gridSize; cy++) {
            const affectedSquares = [];
            const radius = Math.floor(Math.sqrt(radiusSquared));

            const lowerBoundX = Math.max(0, cx - radius);
            const upperBoundX = Math.min(gridSize, cx + radius + 1);
            const lowerBoundY = Math.max(0, cy - radius);
            const upperBoundY = Math.min(gridSize, cy + radius + 1);

            for (let x = lowerBoundX; x < upperBoundX; x++) {
                for (let y = lowerBoundY; y < upperBoundY; y++) {
                    if ((cx - cy) ** 2 + (x - y + 1.0) ** 2 <= radiusSquared) {
                        affectedSquares.push([x, y]);
                    }
                }
            }
            impactDict.set(`${cx},${cy}`, affectedSquares);
        }
    }

    for (const [center, affectedSquares] of impactDict) {
        const [cx, cy] = center.split(',').map(Number);
        const count = affectedSquares.filter(([x, y]) =>
            enemyLocations.has(`${x},${y}`)).length;

        if (count > bestCount) {
            bestCount = count;
            bestCenter = [cx, cy];
        }
    }

    const bestImpactArea = impactDict.get(`${bestCenter[0]},${bestCenter[1]}`);
    for (const [x, y] of bestImpactArea) {
        if (enemyLocations.has(`${x},${y}`)) {
            grid[y][x] = burntEnemyMark;
        } else {
            grid[y][x] = fireballBlastMark;
        }
    }

    for (const row of grid) {
        console.log(row.join(' '));
    }
    console.log(`Best fireball center: (${bestCenter[0]}, ${bestCenter[1]})`);
}

function generateRandomEnemies(count = 15) {
    return Array(count).fill().map(() => [
        Math.floor(Math.random() * 24),
        Math.floor(Math.random() * 24)
    ]);
}

const foes = generateRandomEnemies();
calculateFireballPlacement(foes);
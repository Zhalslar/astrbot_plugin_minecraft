/**
 * 方块类型定义 - 独立模块，避免循环依赖
 */

/* ============================================
   方块类型定义
   ============================================ */
export const BlockType = {
    AIR: 0,
    GRASS: 1,
    DIRT: 2,
    STONE: 3,
    SAND: 4,
    WOOD: 5,
    LEAVES: 6,
};

/** 方块名称映射（用于 HUD 显示） */
export const BlockNames = {
    [BlockType.AIR]: '空气',
    [BlockType.GRASS]: '草方块',
    [BlockType.DIRT]: '泥土',
    [BlockType.STONE]: '石头',
    [BlockType.SAND]: '沙子',
    [BlockType.WOOD]: '木头',
    [BlockType.LEAVES]: '树叶',
};

/** 判断方块是否为实体（非空气） */
export function isSolid(type) {
    return type !== BlockType.AIR;
}

/** 获取方块颜色（用于调试和 HUD） */
export function getBlockColor(type) {
    switch (type) {
        case BlockType.GRASS: return '#4CAF50';
        case BlockType.DIRT: return '#8D6E63';
        case BlockType.STONE: return '#9E9E9E';
        case BlockType.SAND: return '#FFD54F';
        case BlockType.WOOD: return '#795548';
        case BlockType.LEAVES: return '#2E7D32';
        default: return '#E0E0E0';
    }
}
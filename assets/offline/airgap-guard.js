"use strict";

function assertAirGapSource(source) {
  const resourceScheme = /(?:https?|wss?|ftp|file|javascript|data|blob):|\/\//i;
  const resourceDirective = /^\s*(?:click\b|!include\b)|\b(?:src|href)\s*=|@import\b|\burl\s*\(|\b(?:img|image|icon)\s*:/im;
  if (resourceScheme.test(source) || resourceDirective.test(source)) {
    throw new Error("Air-gap policy: resource URLs, includes, images, styles, and clickable links are not allowed. Use plain labels and bundled notation.");
  }
}

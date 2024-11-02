module.exports = {
  transform: {
    "^.+\\.js$": "babel-jest",    
    "^.+\\.vue$": "vue-jest"       
  },
  moduleFileExtensions: ["js", "json", "vue"],
  transformIgnorePatterns: [
    "/node_modules/(?!jest-runtime)"
  ],
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageProvider: "v8"
};
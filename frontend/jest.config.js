module.exports = {
  transform: {
    "^.+\\.js$": "babel-jest",    
    "^.+\\.vue$": "vue-jest"       
  },
  moduleFileExtensions: ["js", "json", "vue"],
  transformIgnorePatterns: [
    "/node_modules/(?!jest-runtime)"
  ],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js'
  },
};

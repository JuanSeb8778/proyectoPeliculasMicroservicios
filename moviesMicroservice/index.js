// index.js
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const movieRouter = require('./routes/movieRouter');

const app = express();
app.use(express.json());

// Swagger setup
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Movies API (Repository Pattern)',
      version: '1.0.0',
      description: 'API para gestionar películas',
    },
  },
  apis: ['./routes/*.js'],
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// Routes
app.use('/movies', movieRouter);

// Start server
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Movies microservice running on port ${PORT}`);
});

const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const userMovieListRouter = require('./routes/userMovieListRouter');

const app = express();
app.use(express.json());

// Configuración de Swagger
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'UserMovieList API (Repository Pattern)',
      version: '1.0.0',
      description: 'API para gestionar las listas de películas de los usuarios',
    },
  },
  apis: ['./routes/*.js'], // <- Muy importante: apunta a tus rutas
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// Usar rutas
app.use('/user-movie-list', userMovieListRouter);

// Arrancar servidor
const PORT = 3002;
app.listen(PORT, () => {
  console.log(`UserMovieList microservice running on port ${PORT}`);
});

const mariadb = require('mariadb');

const pool = mariadb.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Nacional15!',
  database: 'movies_db',
  connectionLimit: 5
});
async function testConnection() {
  try {
    const conn = await pool.getConnection();
    console.log('✅ Conectado correctamente a MariaDB');
    conn.release();
  } catch (err) {
    console.error('❌ Error al conectar con MariaDB:', err.message);
  }
}

testConnection();


module.exports = pool;

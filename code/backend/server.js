require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
// 将原来的引用修改为
const userRoutes = require('./routes/users');
const taskRoutes = require('./routes/tasks');

const app = express();

// 中间件
app.use(cors());
app.use(express.json());

// 路由
app.use('/api/users', userRoutes);
app.use('/api/tasks', taskRoutes);

// 连接数据库并启动服务器
mongoose.connect(process.env.MONGODB_URI)
  .then(() => {
    app.listen(process.env.PORT, () => {
      console.log(`服务器运行在 http://localhost:${process.env.PORT}`);
    });
  })
  .catch(err => console.error('数据库连接失败:', err));
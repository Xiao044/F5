require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors'); // 只保留这一行cors引入
const userRoutes = require('./routes/users');
const taskRoutes = require('./routes/tasks');

const app = express();

// 中间件
app.use(cors()); // 只保留这一行cors使用
app.use(express.json());
app.use(express.static('../frontend')); // 添加静态文件服务

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
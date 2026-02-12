// Vercel Serverless Function for WeChat Verification
module.exports = async (req, res) => {
  const { method } = req;
  
  // 设置CORS头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (method === 'OPTIONS') {
    // 处理预检请求
    res.status(200).end();
    return;
  }
  
  if (method === 'GET') {
    // 微信接口验证
    const { signature, timestamp, nonce, echostr } = req.query;
    
    console.log('📨 收到微信验证请求:', {
      signature,
      timestamp, 
      nonce,
      echostr
    });
    
    // 返回echostr完成验证
    res.setHeader('Content-Type', 'text/plain');
    res.status(200).send(echostr || '');
    
  } else if (method === 'POST') {
    // 处理微信消息
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    
    req.on('end', () => {
      console.log('📨 收到微信消息:', body);
      res.setHeader('Content-Type', 'text/plain');
      res.status(200).send('success');
    });
    
  } else {
    res.status(405).send('Method Not Allowed');
  }
};
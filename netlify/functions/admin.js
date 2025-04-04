const { spawn } = require('child_process');

exports.handler = async (event, context) => {
  const path = event.path.replace(/^\/\.netlify\/functions\/admin/, '');
  const method = event.httpMethod;
  const requestId = context.awsRequestId;
  
  console.log(`[${requestId}] Handling ${method} request to admin${path}`);
  
  try {
    return await runDjangoAdmin(event, context);
  } catch (error) {
    console.error(`[${requestId}] Error:`, error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: `Server error: ${error.message}` })
    };
  }
};

async function runDjangoAdmin(event, context) {
  const { httpMethod, body, queryStringParameters, headers, path } = event;
  const adminPath = path.replace(/^\/\.netlify\/functions\/admin/, '');
  
  console.log(`Running Django Admin with path: ${adminPath}`);
  
  // Netlify Functions o'zgaruvchini o'rnatish
  process.env.RUNNING_IN_NETLIFY = 'true';
  process.env.ADMIN_REQUEST = 'true';
  
  // wsgi.py appni ishga tushirish
  const python = spawn('python', ['wsgi.py', httpMethod, adminPath, JSON.stringify({
    body: body || "",
    queryParams: queryStringParameters || {},
    headers: headers || {}
  })]);
  
  return new Promise((resolve, reject) => {
    let dataChunks = [];
    let errorChunks = [];
    
    python.stdout.on('data', (data) => {
      dataChunks.push(data);
    });
    
    python.stderr.on('data', (data) => {
      errorChunks.push(data);
    });
    
    python.on('close', (code) => {
      if (code !== 0) {
        const errorOutput = Buffer.concat(errorChunks).toString();
        console.error('Python process failed:', errorOutput);
        return reject(new Error(`Python process exited with code ${code}. ${errorOutput}`));
      }
      
      try {
        const result = Buffer.concat(dataChunks).toString();
        const [statusLine, ...contentLines] = result.split('\n');
        const statusCode = parseInt(statusLine, 10);
        const content = contentLines.join('\n');
        
        resolve({
          statusCode,
          body: content,
          headers: {
            'Content-Type': 'text/html',
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  });
} 
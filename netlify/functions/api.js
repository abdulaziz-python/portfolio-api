const { spawn } = require('child_process');

exports.handler = async (event, context) => {
  const path = event.path.replace(/^\/\.netlify\/functions\/api/, '');
  const method = event.httpMethod;
  const requestId = context.awsRequestId;
  
  console.log(`[${requestId}] Handling ${method} request to ${path}`);
  
  try {
    return await runDjangoAPI(event, context);
  } catch (error) {
    console.error(`[${requestId}] Error:`, error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: `Server error: ${error.message}` })
    };
  }
};

async function runDjangoAPI(event, context) {
  const { httpMethod, body, queryStringParameters, headers, path } = event;
  const apiPath = path.replace(/^\/\.netlify\/functions\/api/, '');
  
  console.log(`Running Django API with path: ${apiPath}`);
  
  // Netlify Functions o'zgaruvchini o'rnatish
  process.env.RUNNING_IN_NETLIFY = 'true';
  
  // wsgi.py appni ishga tushirish
  const python = spawn('python', ['wsgi.py', httpMethod, apiPath, JSON.stringify({
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
            'Content-Type': 'application/json',
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  });
} 
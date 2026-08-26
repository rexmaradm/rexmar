export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Método no permitido', { status: 405 });
    }

    const formData = await request.formData();
    let message = 'Nuevo mensaje de contacto:\n\n';
    
    for (const [key, value] of formData.entries()) {
      message += `${key}: ${value}\n`;
    }

    const tgUrl = `https://api.telegram.org/bot${env.TG_TOKEN}/sendMessage`;
    const res = await fetch(tgUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: env.CHAT_ID,
        text: message
      })
    });
  if (res.ok) {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Mensaje enviado</title>
    </head>
    <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
      <h2>¡Mensaje enviado con éxito!</h2>
      <p>Gracias por contactarnos. Te responderemos a la brevedad.</p>
      <a href="https://th.org.pe" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">Volver al inicio</a>
    </body>
    </html>
  `;
  return new Response(html, {
    status: 200,
    headers: { 'Content-Type': 'text/html; charset=utf-8' }
  });
} 
 
  const errorText = await res.text();
   return new Response('Error de Telegram: ' + errorText, { status: 500 });

  }
};

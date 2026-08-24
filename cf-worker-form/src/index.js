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
     return new Response('¡Mensaje enviado con éxito a Telegram!', { status: 200 });
   }
   
   const errorText = await res.text();
   return new Response('Error de Telegram: ' + errorText, { status: 500 });

  }
};

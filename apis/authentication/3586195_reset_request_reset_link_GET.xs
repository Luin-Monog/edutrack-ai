// Request a one-time magic link to reset password
query "reset/request-reset-link" verb=GET {
  api_group = "Authentication"

  input {
    email email?
  }

  stack {
    // Generate a one-time magic link
    function.run "Getting Started Template/generate_magic_link" {
      input = {email: $input.email}
    } as $token_and_email
  
    // Check that the link exists
    precondition ($token_and_email != null) {
      error = "Magic link could not be created. Try again."
    }
  
    // Create a variable with the API base URL
    var $api_base_url {
      value = $env.$api_baseurl
    }
  
    // Create magic link
    var $magic_link {
      value = $api_base_url ~ "/1_start_here_demo_page#/update-password" ~ "?magic_token=" ~ $token_and_email.token ~ "&email=" ~ $token_and_email.email
    }
  
    // Create HTML message with the reset code visible for use in the app
    util.template_engine {
      value = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Redefinição de Senha — EduTrack AI</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h2>Redefinição de Senha — EduTrack AI</h2>
            <p>Olá,</p>
            <p>Recebemos uma solicitação para redefinir sua senha. Use o código abaixo no aplicativo EduTrack AI:</p>
            <div style="text-align: center; margin: 30px 0;">
              <span style="display: inline-block; padding: 16px 32px; background-color: #1e293b; color: #ffffff; font-size: 22px; font-family: monospace; letter-spacing: 4px; border-radius: 8px;">
                {{ $token_and_email.token }}
              </span>
            </div>
            <p>Cole esse código na tela de <strong>Esqueci minha senha</strong> do EduTrack AI junto com sua nova senha.</p>
            <p>O código expira em 24 horas e só pode ser usado uma vez.</p>
            <p>Se você não solicitou a redefinição, ignore este e-mail.</p>
          </div>
        </body>
        </html>
        """
    } as $message
  
    // Send Email Function will ONLY send to the instance owner email with the free credits. Provide your own Resend API key and account for additional capability.
  
    // Send email with password reset link
    util.send_email {
      service_provider = "xano"
      subject = "Your password reset request"
      message = $message
    } as $send_email
  }

  response = {
    message: {}|set:"success":true|set:"message":"magic link sent"
  }

  tags = ["xano:quick-start"]
}
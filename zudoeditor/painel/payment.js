// Script para o sistema de pagamento

document.addEventListener('DOMContentLoaded', function() {
    // Manipulação dos métodos de pagamento
    const paymentMethods = document.querySelectorAll('input[name="payment"]');
    const paymentButton = document.querySelector('.payment-action .btn-large');
    
    if (paymentMethods && paymentButton) {
        paymentMethods.forEach(method => {
            method.addEventListener('change', function() {
                // Alterar o link do botão de pagamento com base no método selecionado
                if (this.id === 'pix') {
                    paymentButton.setAttribute('href', 'https://mpago.la/2Afm7Ld');
                    paymentButton.textContent = 'Pagar com PIX';
                } else if (this.id === 'credit-card') {
                    paymentButton.setAttribute('href', 'https://mpago.la/2Afm7Ld');
                    paymentButton.textContent = 'Pagar com Cartão';
                } else if (this.id === 'bank-transfer') {
                    paymentButton.setAttribute('href', '#');
                    paymentButton.textContent = 'Ver Dados Bancários';
                    
                    // Mostrar modal ou alerta com dados bancários
                    paymentButton.addEventListener('click', function(e) {
                        if (this.textContent === 'Ver Dados Bancários') {
                            e.preventDefault();
                            alert('Dados para Transferência Bancária:\n\nNome: Ricardo Moreno\nConta: 47264213870\n\nApós a transferência, envie o comprovante para rickmorenosan@gmail.com');
                        }
                    });
                }
            });
        });
    }
    
    // Formulário de contato para envio de comprovante
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simular envio do formulário
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            submitButton.disabled = true;
            submitButton.textContent = 'Enviando...';
            
            // Simular atraso de envio
            setTimeout(function() {
                alert('Comprovante enviado com sucesso! Entraremos em contato em breve.');
                contactForm.reset();
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }, 1500);
        });
    }
    
    // Botão de download do tutorial em PDF
    const tutorialButton = document.querySelector('a[href="tutorial_completo.pdf"]');
    
    if (tutorialButton) {
        tutorialButton.addEventListener('click', function(e) {
            // Verificar se o arquivo existe antes de tentar baixar
            // Neste caso, apenas mostramos uma mensagem informativa
            // Em produção, este código seria removido quando o PDF estiver disponível
            e.preventDefault();
            alert('O tutorial completo será disponibilizado após a finalização da compra. Para a versão gratuita, um tutorial básico será enviado por e-mail.');
        });
    }
});

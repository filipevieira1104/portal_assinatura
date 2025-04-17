/**
 * Sistema de Assinaturas - JavaScript Principal
 * 
 * Este arquivo contém funções e utilitários para aprimorar a experiência do usuário
 * com elementos interativos e visuais que complementam o tema tecnológico.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Remover o preloader imediatamente
    hidePreloader();
    
    // Inicializar componentes de interface
    initializeComponents();
    
    // Animações de entrada para cards e elementos
    animateElements();
    
    // Adicionar efeitos de hover aos cards
    setupCardEffects();
    
    // Configurar máscaras de input
    setupInputMasks();
    
    // Habilitação condicional de botões
    setupConditionalButtons();
    
    // Adicionar tooltips para ícones e ações
    setupTooltips();
});

// Garantir que o preloader seja removido mesmo se houver algum problema
window.addEventListener('load', hidePreloader);

// Definir um tempo máximo para o preloader (3 segundos)
setTimeout(hidePreloader, 3000);

/**
 * Remove o preloader da tela
 */
function hidePreloader() {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.style.opacity = '0';
        setTimeout(function() {
            preloader.style.display = 'none';
        }, 300);
    }
}

/**
 * Inicializa componentes de interface geral
 */
function initializeComponents() {
    // Dropdown de usuário aprimorado
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        userDropdown.addEventListener('show.bs.dropdown', function() {
            document.querySelector('.dropdown-menu').classList.add('animated', 'fadeIn');
        });
    }
    
    // Animar barra de progresso
    const progressBars = document.querySelectorAll('.progress-bar');
    if (progressBars.length > 0) {
        progressBars.forEach(bar => {
            const targetWidth = bar.getAttribute('aria-valuenow') + '%';
            setTimeout(() => {
                bar.style.width = targetWidth;
            }, 200);
        });
    }
    
    // Botões com efeitos de onda ao clicar
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

/**
 * Adiciona animações aos elementos da página ao carregar
 */
function animateElements() {
    // Animar entrada de cards
    const cards = document.querySelectorAll('.card, .dashboard-card');
    if (cards.length > 0) {
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 + (index * 50));
        });
    }
    
    // Animar contadores
    const counters = document.querySelectorAll('.counter-value');
    if (counters.length > 0) {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'), 10);
            let count = 0;
            const increment = target / 30; // Velocidade da animação
            
            const updateCount = () => {
                if (count < target) {
                    count += increment;
                    counter.innerText = Math.ceil(count);
                    setTimeout(updateCount, 30);
                } else {
                    counter.innerText = target;
                }
            };
            
            updateCount();
        });
    }
}

/**
 * Configura efeitos visuais para cards
 */
function setupCardEffects() {
    // Efeito de paralaxe suave para cards
    const cards = document.querySelectorAll('.card-hover-effect');
    if (cards.length > 0) {
        cards.forEach(card => {
            card.addEventListener('mousemove', function(e) {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            
            card.addEventListener('mouseleave', function() {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
                card.style.transition = 'transform 0.5s ease';
            });
        });
    }
}

/**
 * Configura máscaras de input para formulários
 */
function setupInputMasks() {
    // Máscara para CPF
    const cpfInputs = document.querySelectorAll('input[id="cpf"]');
    if (cpfInputs.length > 0) {
        cpfInputs.forEach(input => {
            input.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 11) value = value.slice(0, 11);
                
                if (value.length > 9) {
                    value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{0,2})/, '$1.$2.$3-$4');
                } else if (value.length > 6) {
                    value = value.replace(/(\d{3})(\d{3})(\d{0,3})/, '$1.$2.$3');
                } else if (value.length > 3) {
                    value = value.replace(/(\d{3})(\d{0,3})/, '$1.$2');
                }
                
                e.target.value = value;
            });
        });
    }
    
    // Máscara para CEP
    const cepInputs = document.querySelectorAll('input[id="cep"]');
    if (cepInputs.length > 0) {
        cepInputs.forEach(input => {
            input.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 8) value = value.slice(0, 8);
                
                if (value.length > 5) {
                    value = value.replace(/(\d{5})(\d{0,3})/, '$1-$2');
                }
                
                e.target.value = value;
                
                // Buscar CEP via API quando completo
                if (value.length === 9) {
                    buscarEnderecoPorCEP(value);
                }
            });
        });
    }
    
    // Máscara para telefone
    const telefoneInputs = document.querySelectorAll('input[id^="telefone"], input[id="id_telefone"]');
    if (telefoneInputs.length > 0) {
        telefoneInputs.forEach(input => {
            input.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 11) value = value.slice(0, 11);
                
                if (value.length > 6) {
                    value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
                } else if (value.length > 2) {
                    value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
                }
                
                e.target.value = value;
            });
        });
    }
}

/**
 * Configura tooltips para elementos de interface
 */
function setupTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
}

/**
 * Configura botões condicionais baseados em checkboxes ou outros inputs
 */
function setupConditionalButtons() {
    // Checkbox "concordo" para habilitar botão
    const checkboxConsentimentos = document.querySelectorAll('input[type="checkbox"][id="concordo"]');
    if (checkboxConsentimentos.length > 0) {
        checkboxConsentimentos.forEach(checkbox => {
            const botaoAlvo = document.getElementById('btnAbrirModal');
            if (botaoAlvo) {
                // Configurar estado inicial
                botaoAlvo.disabled = !checkbox.checked;
                
                // Adicionar listener
                checkbox.addEventListener('change', function() {
                    botaoAlvo.disabled = !this.checked;
                    
                    if (this.checked) {
                        botaoAlvo.classList.add('btn-pulse');
                    } else {
                        botaoAlvo.classList.remove('btn-pulse');
                    }
                });
            }
        });
    }
}

/**
 * Busca o endereço pelo CEP usando a API ViaCEP
 * @param {string} cep CEP formatado ou não
 */
function buscarEnderecoPorCEP(cep) {
    cep = cep.replace(/\D/g, '');
    
    if (cep.length !== 8) return;
    
    // Mostrar indicador de carregamento
    const cepInput = document.getElementById('cep');
    if (cepInput) {
        cepInput.classList.add('loading');
    }
    
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (!data.erro) {
                const campos = {
                    'endereco': data.logradouro,
                    'bairro': data.bairro,
                    'cidade': data.localidade,
                    'estado': data.uf
                };
                
                // Preencher os campos com os dados retornados
                Object.keys(campos).forEach(id => {
                    const campo = document.getElementById(id);
                    if (campo) {
                        campo.value = campos[id];
                        // Adicionar efeito de destaque ao preencher
                        campo.classList.add('field-highlight');
                        setTimeout(() => {
                            campo.classList.remove('field-highlight');
                        }, 1000);
                    }
                });
                
                // Foca no campo número após preencher
                const numeroInput = document.getElementById('numero');
                if (numeroInput) numeroInput.focus();
            }
        })
        .catch(error => console.error('Erro ao buscar CEP:', error))
        .finally(() => {
            // Remover indicador de carregamento
            if (cepInput) {
                cepInput.classList.remove('loading');
            }
        });
} 
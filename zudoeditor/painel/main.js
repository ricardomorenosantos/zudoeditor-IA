// Script principal para o site do Software de Automação de Vídeos

document.addEventListener('DOMContentLoaded', function() {
    // Menu móvel
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('nav ul');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('open');
        });
    }
    
    // FAQ accordion
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', function() {
            // Fechar outros itens
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Alternar estado atual
            item.classList.toggle('active');
        });
    });
    
    // Submenu da documentação
    const docMenuItems = document.querySelectorAll('.docs-menu > li');
    
    docMenuItems.forEach(item => {
        const link = item.querySelector('a');
        const submenu = item.querySelector('.submenu');
        
        if (submenu) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                submenu.classList.toggle('open');
            });
        }
    });
    
    // Animação de entrada para elementos
    const animateElements = document.querySelectorAll('.animate-fade-in');
    
    function checkScroll() {
        animateElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight * 0.9) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Inicializar elementos com opacidade 0
    animateElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
    });
    
    // Verificar posição inicial
    checkScroll();
    
    // Verificar ao rolar
    window.addEventListener('scroll', checkScroll);
    
    // Smooth scroll para links de âncora
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href !== '#!') {
                e.preventDefault();
                
                const target = document.querySelector(href);
                
                if (target) {
                    const headerHeight = document.querySelector('header').offsetHeight;
                    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
                    
                    window.scrollTo({
                        top: targetPosition - headerHeight - 20,
                        behavior: 'smooth'
                    });
                    
                    // Fechar menu móvel se estiver aberto
                    if (navMenu.classList.contains('open')) {
                        navMenu.classList.remove('open');
                    }
                }
            }
        });
    });
    
    // Destacar link ativo na navegação
    function setActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('nav a[href^="#"]');
        
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const headerHeight = document.querySelector('header').offsetHeight;
            
            if (window.scrollY >= sectionTop - headerHeight - 100) {
                currentSection = '#' + section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentSection) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', setActiveNavLink);
    
    // Inicializar link ativo
    setActiveNavLink();
    
    // Código específico para a página de documentação
    if (document.querySelector('.docs-container')) {
        // Destacar link ativo na navegação da documentação
        function setActiveDocLink() {
            const headings = document.querySelectorAll('.docs-content h2[id], .docs-content h3[id]');
            const docLinks = document.querySelectorAll('.docs-menu a[href^="#"]');
            
            let currentHeading = '';
            
            headings.forEach(heading => {
                const headingTop = heading.offsetTop;
                const headerHeight = document.querySelector('header').offsetHeight;
                
                if (window.scrollY >= headingTop - headerHeight - 100) {
                    currentHeading = '#' + heading.getAttribute('id');
                }
            });
            
            docLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === currentHeading) {
                    link.classList.add('active');
                    
                    // Abrir submenu pai se necessário
                    const parentLi = link.closest('li');
                    const parentUl = parentLi.closest('ul');
                    
                    if (parentUl.classList.contains('submenu')) {
                        parentUl.classList.add('open');
                    }
                }
            });
        }
        
        window.addEventListener('scroll', setActiveDocLink);
        
        // Inicializar link ativo
        setActiveDocLink();
    }
});

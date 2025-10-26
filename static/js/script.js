// static/js/dashboard.js

// Gráfico de ingresos diarios
function inicializarGraficoDiario(diasLabels, ingresosDatos) {
    const ctxDiario = document.getElementById('ingresosDiariosChart');
    if (!ctxDiario) return;
    
    new Chart(ctxDiario.getContext('2d'), {
        type: 'line',
        data: {
            labels: diasLabels,
            datasets: [{
                label: 'Ingresos',
                data: ingresosDatos,
                backgroundColor: 'rgba(78, 115, 223, 0.1)',
                borderColor: 'rgba(78, 115, 223, 1)',
                pointBackgroundColor: 'rgba(78, 115, 223, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(78, 115, 223, 1)'
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de ingresos mensuales
function inicializarGraficoMensual(mesesLabels, ingresosDatos) {
    const ctxMensual = document.getElementById('ingresosMensualesChart');
    if (!ctxMensual) return;
    
    new Chart(ctxMensual.getContext('2d'), {
        type: 'bar',
        data: {
            labels: mesesLabels,
            datasets: [{
                label: 'Ingresos',
                data: ingresosDatos,
                backgroundColor: 'rgba(28, 200, 138, 0.6)',
                borderColor: 'rgba(28, 200, 138, 1)',
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                }
            }
        }
    });
}

// Notificaciones laterales
function inicializarNotificaciones() {
    console.log('Inicializando notificaciones laterales...');
    
    // Mostrar notificaciones después de un delay
    setTimeout(function() {
        const notificacionesIzquierda = document.querySelector('.notificacion-izquierda');
        const notificacionesDerecha = document.querySelector('.notificacion-derecha');
        
        console.log('Notificaciones izquierda:', notificacionesIzquierda?.children.length);
        console.log('Notificaciones derecha:', notificacionesDerecha?.children.length);
        
        if (notificacionesIzquierda && notificacionesIzquierda.children.length > 0) {
            notificacionesIzquierda.classList.add('mostrar');
            console.log('Mostrando notificaciones izquierda');
        }
        
        if (notificacionesDerecha && notificacionesDerecha.children.length > 0) {
            notificacionesDerecha.classList.add('mostrar');
            console.log('Mostrando notificaciones derecha');
        }
    }, 1000);
    
    // Ocultar notificaciones al hacer clic
    document.addEventListener('click', function(e) {
        if (e.target.closest('.notificacion-card')) {
            const card = e.target.closest('.notificacion-card');
            card.style.opacity = '0';
            card.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                card.remove();
                console.log('Notificación eliminada');
                
                // Si no quedan notificaciones, ocultar el contenedor
                const contenedor = card.closest('.notificacion-lateral');
                if (contenedor && contenedor.children.length === 0) {
                    contenedor.classList.remove('mostrar');
                    console.log('Contenedor de notificaciones vacío, ocultando...');
                }
            }, 300);
        }
    });
    
    // Actualizar notificaciones cada 30 segundos
    function actualizarNotificaciones() {
        fetch('/api/notificaciones')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Notificaciones actualizadas:', data);
                    // Aquí puedes añadir lógica para actualizar dinámicamente
                }
            })
            .catch(error => console.error('Error al actualizar notificaciones:', error));
    }
    
    setInterval(actualizarNotificaciones, 30000);
}

// Función principal que inicializa todo el dashboard
function inicializarDashboard(diasLabels, ingresosDiarios, mesesLabels, ingresosMensuales) {
    console.log('Inicializando dashboard...');
    
    // Inicializar gráficos
    inicializarGraficoDiario(diasLabels, ingresosDiarios);
    inicializarGraficoMensual(mesesLabels, ingresosMensuales);
    
    // Inicializar notificaciones
    inicializarNotificaciones();
    
    console.log('Dashboard inicializado correctamente');
}

// Exportar funciones para uso global
window.inicializarDashboard = inicializarDashboard;
window.inicializarGraficoDiario = inicializarGraficoDiario;
window.inicializarGraficoMensual = inicializarGraficoMensual;
window.inicializarNotificaciones = inicializarNotificaciones;


// Script para mejorar el navbar
document.addEventListener('DOMContentLoaded', function() {
    // Ajustar navbar en scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 20) {
            navbar.style.padding = '4px 0';
            navbar.style.boxShadow = '0 2px 10px rgba(39, 174, 96, 0.2)';
        } else {
            navbar.style.padding = '8px 0';
            navbar.style.boxShadow = '0 4px 20px rgba(39, 174, 96, 0.3)';
        }
    });
    
    // Cerrar navbar en móvil al hacer clic
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            }
        });
    });
});
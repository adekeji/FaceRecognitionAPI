// Kubernetes Bare Metal Installation Tutorial JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Update URL without causing page jump
                history.pushState(null, null, targetId);
            }
        });
    });

    // Code block copy functionality
    addCopyButtons();
    
    // Progress tracking
    trackProgress();
    
    // Mobile menu toggle (if needed)
    handleMobileNavigation();
    
    // Command validation
    addCommandValidation();
});

function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('.code-block pre');
    
    codeBlocks.forEach((block, index) => {
        // Skip if it's just a description, not actual code
        const text = block.textContent.trim();
        if (!text.includes('#') && !text.includes('sudo') && !text.includes('kubectl')) {
            return;
        }
        
        const container = block.parentElement;
        container.style.position = 'relative';
        
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-btn';
        copyButton.innerHTML = '📋 Copy';
        copyButton.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #3498db;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            z-index: 10;
        `;
        
        copyButton.addEventListener('click', function() {
            // Clean up the text for copying
            const cleanText = text
                .split('\n')
                .filter(line => line.trim() && !line.trim().startsWith('#'))
                .map(line => line.trim())
                .join('\n');
                
            navigator.clipboard.writeText(cleanText).then(() => {
                copyButton.innerHTML = '✅ Copied!';
                copyButton.style.background = '#27ae60';
                
                setTimeout(() => {
                    copyButton.innerHTML = '📋 Copy';
                    copyButton.style.background = '#3498db';
                }, 2000);
            }).catch(() => {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = cleanText;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                copyButton.innerHTML = '✅ Copied!';
                setTimeout(() => {
                    copyButton.innerHTML = '📋 Copy';
                }, 2000);
            });
        });
        
        container.appendChild(copyButton);
    });
}

function trackProgress() {
    // Add checkboxes to track completion of steps
    const steps = document.querySelectorAll('.step');
    
    steps.forEach((step, index) => {
        const stepId = `step-${index}`;
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = stepId;
        checkbox.className = 'step-checkbox';
        checkbox.style.cssText = `
            margin-right: 10px;
            transform: scale(1.2);
        `;
        
        // Load saved state
        const isCompleted = localStorage.getItem(stepId) === 'true';
        checkbox.checked = isCompleted;
        if (isCompleted) {
            step.style.background = '#d5f4e6';
            step.style.borderLeftColor = '#27ae60';
        }
        
        checkbox.addEventListener('change', function() {
            localStorage.setItem(stepId, this.checked);
            if (this.checked) {
                step.style.background = '#d5f4e6';
                step.style.borderLeftColor = '#27ae60';
            } else {
                step.style.background = '';
                step.style.borderLeftColor = '#3498db';
            }
            updateProgressBar();
        });
        
        const heading = step.querySelector('h4');
        if (heading) {
            const label = document.createElement('label');
            label.htmlFor = stepId;
            label.style.cssText = `
                display: flex;
                align-items: center;
                cursor: pointer;
                margin-bottom: 1rem;
            `;
            
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(heading.textContent));
            
            heading.style.display = 'none';
            step.insertBefore(label, step.firstChild);
        }
    });
    
    updateProgressBar();
}

function updateProgressBar() {
    let progressContainer = document.querySelector('.progress-container');
    
    if (!progressContainer) {
        progressContainer = document.createElement('div');
        progressContainer.className = 'progress-container';
        progressContainer.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            min-width: 200px;
        `;
        document.body.appendChild(progressContainer);
    }
    
    const checkboxes = document.querySelectorAll('.step-checkbox');
    const completedSteps = document.querySelectorAll('.step-checkbox:checked').length;
    const totalSteps = checkboxes.length;
    const progressPercentage = totalSteps > 0 ? Math.round((completedSteps / totalSteps) * 100) : 0;
    
    progressContainer.innerHTML = `
        <h4 style="margin-bottom: 10px; color: #2c3e50;">Installation Progress</h4>
        <div style="background: #ecf0f1; height: 10px; border-radius: 5px; overflow: hidden;">
            <div style="background: #3498db; height: 100%; width: ${progressPercentage}%; transition: width 0.3s ease;"></div>
        </div>
        <p style="margin-top: 10px; text-align: center; color: #555;">
            ${completedSteps}/${totalSteps} steps completed (${progressPercentage}%)
        </p>
    `;
}

function handleMobileNavigation() {
    // Add mobile menu toggle if screen is small
    if (window.innerWidth <= 768) {
        const nav = document.querySelector('nav');
        const navList = document.querySelector('nav ul');
        
        const menuToggle = document.createElement('button');
        menuToggle.innerHTML = '☰ Menu';
        menuToggle.style.cssText = `
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            display: none;
            margin: 0 auto 1rem auto;
        `;
        
        if (window.innerWidth <= 768) {
            menuToggle.style.display = 'block';
            navList.style.display = 'none';
        }
        
        menuToggle.addEventListener('click', function() {
            if (navList.style.display === 'none') {
                navList.style.display = 'flex';
                this.innerHTML = '✕ Close';
            } else {
                navList.style.display = 'none';
                this.innerHTML = '☰ Menu';
            }
        });
        
        nav.insertBefore(menuToggle, navList);
    }
}

function addCommandValidation() {
    // Add simple command validation hints
    const codeBlocks = document.querySelectorAll('.code-block pre');
    
    codeBlocks.forEach(block => {
        const text = block.textContent;
        
        // Check for common issues
        if (text.includes('sudo') && text.includes('kubeadm join')) {
            const warning = document.createElement('div');
            warning.style.cssText = `
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 14px;
            `;
            warning.innerHTML = '⚠️ <strong>Note:</strong> Replace the placeholders (&lt;token&gt;, &lt;hash&gt;, &lt;control-plane-ip&gt;) with actual values from your kubeadm init output.';
            
            block.parentElement.appendChild(warning);
        }
        
        if (text.includes('kubectl') && !text.includes('sudo')) {
            const info = document.createElement('div');
            info.style.cssText = `
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                color: #0c5460;
                padding: 10px;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 14px;
            `;
            info.innerHTML = '💡 <strong>Tip:</strong> Make sure kubectl is configured with admin credentials before running these commands.';
            
            block.parentElement.appendChild(info);
        }
    });
}

// Handle window resize
window.addEventListener('resize', function() {
    handleMobileNavigation();
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Press 'h' to go to top
    if (e.key === 'h' && !e.ctrlKey && !e.altKey) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Press 'r' to reset progress
    if (e.key === 'r' && e.ctrlKey) {
        e.preventDefault();
        if (confirm('Reset all progress? This will uncheck all completed steps.')) {
            const checkboxes = document.querySelectorAll('.step-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
                localStorage.removeItem(checkbox.id);
                const step = checkbox.closest('.step');
                if (step) {
                    step.style.background = '';
                    step.style.borderLeftColor = '#3498db';
                }
            });
            updateProgressBar();
        }
    }
});

console.log('🚀 Kubernetes Bare Metal Installation Tutorial loaded successfully!');
console.log('💡 Tips: Press "h" to go to top, Ctrl+R to reset progress');
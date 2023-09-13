window.onload = () => {

            const privacyBannerAcknowledged = document.cookie.split(';').some((item) => item.trim().startsWith('privacy-banner-accepted='));
            const privacyBanner = document.getElementById('privacy-banner-container');
            const dismissButton = document.getElementById('close-privacy');
            const necessaryButton = document.getElementById('accept-necessary');

            if (!privacyBannerAcknowledged) {
                privacyBanner.style.animationDuration = '1.5s';
                privacyBanner.classList.add('slide-up');
                privacyBanner.style.animationFillMode = 'forwards';
            } else {
                privacyBanner.style.display = 'none';
            }

            const closeBanner = () => {
                const date = new Date();
                date.setDate(date.getDate() + 7);
                document.cookie = `privacy-banner-accepted=true; expires=${date.toUTCString()};path=/`;
                let fadeEffect = setInterval(() => {
                    if (!privacyBanner.style.opacity) {
                        privacyBanner.style.opacity = 1;
                    }
                    if (privacyBanner.style.opacity > 0) {
                        privacyBanner.style.opacity -= 0.1;
                    } else {
                        clearInterval(fadeEffect);
                        privacyBanner.style.display = 'none';
                    }
                }, 30);
            };

            dismissButton.onclick = closeBanner;
            necessaryButton.onclick = closeBanner;
        };
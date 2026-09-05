/* ELEMENTS */

const canvas =
    document.getElementById("particleCanvas");

const ctx =
    canvas.getContext("2d");

const logoWrapper =
    document.querySelector(".logo-wrapper");

const brandName =
    document.getElementById("brandName");

const brandType =
    document.getElementById("brandType");

const tagline =
    document.getElementById("tagline");

const loading =
    document.getElementById("loading");


/* PARTICLES */

let particles = [];

const PARTICLE_COUNT = 95;


/* CANVAS SIZE */

function resizeCanvas() {

    const rect =
        canvas.getBoundingClientRect();

    const ratio =
        window.devicePixelRatio || 1;

    canvas.width =
        rect.width * ratio;

    canvas.height =
        rect.height * ratio;

    ctx.setTransform(
        ratio,
        0,
        0,
        ratio,
        0,
        0
    );
}


window.addEventListener(
    "resize",
    resizeCanvas
);

resizeCanvas();


/* PARTICLE CLASS */

class Particle {

    constructor() {

        this.reset();
    }


    reset() {

        const width =
            canvas.clientWidth;

        const height =
            canvas.clientHeight;


        /*
         * Start particles around the outside
         * of the logo area.
         */

        const side =
            Math.floor(
                Math.random() * 4
            );


        if (side === 0) {

            this.x =
                Math.random() * width;

            this.y =
                -20;

        } else if (side === 1) {

            this.x =
                width + 20;

            this.y =
                Math.random() * height;

        } else if (side === 2) {

            this.x =
                Math.random() * width;

            this.y =
                height + 20;

        } else {

            this.x =
                -20;

            this.y =
                Math.random() * height;
        }


        /*
         * Target is near the center.
         */

        this.targetX =
            width / 2 +
            (Math.random() - 0.5) * 210;

        this.targetY =
            height / 2 +
            (Math.random() - 0.5) * 250;


        this.size =
            Math.random() * 2.8 + 0.8;


        this.alpha =
            Math.random() * 0.45 + 0.35;


        this.speed =
            Math.random() * 0.018 + 0.012;


        this.phase =
            Math.random() *
            Math.PI *
            2;


        this.twinkle =
            Math.random() *
            0.03;
    }


    update(progress) {

        /*
         * Ease-out movement.
         */

        const eased =
            1 -
            Math.pow(
                1 - progress,
                3
            );


        this.currentX =
            this.x +
            (
                this.targetX -
                this.x
            ) *
            eased;


        this.currentY =
            this.y +
            (
                this.targetY -
                this.y
            ) *
            eased;


        /*
         * Gentle organic movement.
         */

        this.currentX +=
            Math.sin(
                this.phase +
                progress * 7
            ) * 2;


        this.currentY +=
            Math.cos(
                this.phase +
                progress * 6
            ) * 2;
    }


    draw(progress) {

        const pulse =
            1 +
            Math.sin(
                this.phase +
                progress * 10
            ) * 0.18;


        const alpha =
            this.alpha *
            Math.sin(
                Math.min(
                    progress * Math.PI,
                    Math.PI
                )
            );


        ctx.beginPath();


        ctx.arc(
            this.currentX,
            this.currentY,
            this.size * pulse,
            0,
            Math.PI * 2
        );


        ctx.fillStyle =
            `rgba(108, 174, 87, ${alpha})`;


        ctx.fill();
    }
}


/* CREATE PARTICLES */

function createParticles() {

    particles = [];

    for (
        let i = 0;
        i < PARTICLE_COUNT;
        i++
    ) {

        particles.push(
            new Particle()
        );
    }
}


/* PARTICLE ANIMATION */

function animateParticles(
    startTime
) {

    const elapsed =
        performance.now() -
        startTime;


    /*
     * Particles converge for 2.6 seconds.
     */

    const duration =
        2600;


    const progress =
        Math.min(
            elapsed / duration,
            1
        );


    ctx.clearRect(
        0,
        0,
        canvas.clientWidth,
        canvas.clientHeight
    );


    particles.forEach(
        particle => {

            particle.update(
                progress
            );

            particle.draw(
                progress
            );
        }
    );


    if (progress < 1) {

        requestAnimationFrame(
            () =>
                animateParticles(
                    startTime
                )
        );
    }

}


/* PARTICLE DISPERSION */

function disperseParticles() {

    const start =
        performance.now();


    const duration =
        1700;


    function frame() {

        const elapsed =
            performance.now() -
            start;


        const progress =
            Math.min(
                elapsed / duration,
                1
            );


        ctx.clearRect(
            0,
            0,
            canvas.clientWidth,
            canvas.clientHeight
        );


        particles.forEach(
            particle => {

                const angle =
                    Math.atan2(
                        particle.targetY -
                        canvas.clientHeight / 2,

                        particle.targetX -
                        canvas.clientWidth / 2
                    );


                const distance =
                    Math.hypot(
                        particle.targetX -
                        canvas.clientWidth / 2,

                        particle.targetY -
                        canvas.clientHeight / 2
                    );


                const spread =
                    distance +
                    progress * 160;


                particle.currentX =
                    canvas.clientWidth / 2 +
                    Math.cos(angle) *
                    spread;


                particle.currentY =
                    canvas.clientHeight / 2 +
                    Math.sin(angle) *
                    spread;


                const alpha =
                    particle.alpha *
                    (1 - progress);


                ctx.beginPath();


                ctx.arc(
                    particle.currentX,
                    particle.currentY,
                    particle.size,
                    0,
                    Math.PI * 2
                );


                ctx.fillStyle =
                    `rgba(108, 174, 87, ${alpha})`;


                ctx.fill();
            }
        );


        if (progress < 1) {

            requestAnimationFrame(
                frame
            );

        } else {

            ctx.clearRect(
                0,
                0,
                canvas.clientWidth,
                canvas.clientHeight
            );
        }
    }


    requestAnimationFrame(
        frame
    );
}


/* REVEAL LOGO */

function revealLogo() {

    logoWrapper.classList.add(
        "reveal"
    );
}


/* REVEAL BRAND NAME */

function revealBrandName() {

    brandName.classList.add(
        "show"
    );
}


/* REVEAL BRAND TYPE */

function revealBrandType() {

    brandType.classList.add(
        "show"
    );
}


/* REVEAL TAGLINE */

function revealTagline() {

    tagline.classList.add(
        "show"
    );
}


/* SHOW LOADING */

function showLoading() {

    loading.classList.add(
        "show"
    );
}


/* START ANIMATION */

async function startAnimation() {

    /*
     * Make sure everything starts hidden.
     */

    logoWrapper.classList.remove(
        "reveal"
    );

    brandName.classList.remove(
        "show"
    );

    brandType.classList.remove(
        "show"
    );

    tagline.classList.remove(
        "show"
    );

    loading.classList.remove(
        "show"
    );


    /*
     * Create particles.
     */

    createParticles();


    /*
     * Give the screen a moment of calm.
     */

    await wait(700);


    /*
     * Particles begin entering.
     */

    animateParticles(
        performance.now()
    );


    /*
     * Allow particles to gather.
     */

    await wait(1700);


    /*
     * Reveal the actual approved leaf.
     */

    revealLogo();


    /*
     * Let the reveal breathe.
     */

    await wait(850);


    /*
     * Particles move outward.
     */

    disperseParticles();


    await wait(500);


    /*
     * Branding appears sequentially.
     */

    revealBrandName();

    await wait(350);

    revealBrandType();

    await wait(450);

    revealTagline();

    await wait(650);

    showLoading();
}


/* WAIT HELPER */

function wait(ms) {

    return new Promise(
        resolve =>
            setTimeout(
                resolve,
                ms
            )
    );
}


/* START */

window.addEventListener(
    "load",
    () => {

        /*
         * Small delay makes the initial
         * white/light screen feel intentional.
         */

        setTimeout(
            startAnimation,
            300
        );
    }
);
package com.linknode.showcase

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.util.AttributeSet
import android.view.View
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random

class ParticleAnimationView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    private val particles = mutableListOf<Particle>()
    private val paint = Paint().apply {
        isAntiAlias = true
        style = Paint.Style.FILL
    }
    
    private val particleCount = 50
    private var animator: ValueAnimator? = null

    init {
        setLayerType(LAYER_TYPE_HARDWARE, null)
        initParticles()
        startAnimation()
    }

    private fun initParticles() {
        particles.clear()
        repeat(particleCount) {
            particles.add(Particle.random(width.toFloat(), height.toFloat()))
        }
    }

    private fun startAnimation() {
        animator = ValueAnimator.ofFloat(0f, 1f).apply {
            duration = Long.MAX_VALUE
            repeatCount = ValueAnimator.INFINITE
            addUpdateListener {
                updateParticles()
                invalidate()
            }
            start()
        }
    }

    private fun updateParticles() {
        particles.forEach { particle ->
            particle.update()
            
            // Reset particle if it goes off screen
            if (particle.y < -50f || particle.x < -50f || 
                particle.x > width + 50f || particle.y > height + 50f) {
                particle.reset(width.toFloat(), height.toFloat())
            }
        }
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        initParticles()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        particles.forEach { particle ->
            paint.alpha = (particle.alpha * 255).toInt()
            paint.color = particle.color
            canvas.drawCircle(particle.x, particle.y, particle.size, paint)
        }
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        animator?.cancel()
    }

    private data class Particle(
        var x: Float,
        var y: Float,
        var vx: Float,
        var vy: Float,
        var size: Float,
        var alpha: Float,
        var color: Int
    ) {
        fun update() {
            x += vx
            y += vy
            alpha -= 0.002f
            if (alpha < 0) alpha = 0f
        }

        fun reset(maxX: Float, maxY: Float) {
            x = Random.nextFloat() * maxX
            y = maxY + Random.nextFloat() * 100f
            vx = (Random.nextFloat() - 0.5f) * 2f
            vy = -Random.nextFloat() * 2f - 0.5f
            alpha = Random.nextFloat() * 0.5f + 0.3f
            size = Random.nextFloat() * 4f + 2f
        }

        companion object {
            private val colors = intArrayOf(
                0xFFFFFFFF.toInt(),
                0xFFE3F2FD.toInt(),
                0xFFC5CAE9.toInt(),
                0xFFD1C4E9.toInt()
            )

            fun random(maxX: Float, maxY: Float): Particle {
                return Particle(
                    x = Random.nextFloat() * maxX,
                    y = Random.nextFloat() * maxY,
                    vx = (Random.nextFloat() - 0.5f) * 2f,
                    vy = -Random.nextFloat() * 2f - 0.5f,
                    size = Random.nextFloat() * 4f + 2f,
                    alpha = Random.nextFloat() * 0.5f + 0.3f,
                    color = colors.random()
                )
            }
        }
    }
}
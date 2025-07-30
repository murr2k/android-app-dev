package com.linknode.showcase

import android.content.Intent
import android.graphics.drawable.AnimationDrawable
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.ScrollView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.linknode.showcase.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Set status bar color
        window.statusBarColor = ContextCompat.getColor(this, R.color.primary_dark)
        
        // Start animated gradient background
        val animDrawable = binding.heroSection.background as AnimationDrawable
        animDrawable.setEnterFadeDuration(2000)
        animDrawable.setExitFadeDuration(2000)
        animDrawable.start()
        
        // Set up click listeners
        setupClickListeners()
        
        // Add scroll effect to header
        setupScrollEffect()
    }

    private fun setupClickListeners() {
        binding.btnGetStarted.setOnClickListener {
            // Handle get started action
            showComingSoon("Get Started")
        }
        
        binding.btnLearnMore.setOnClickListener {
            // Open linknode.com in browser
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://linknode.com"))
            startActivity(intent)
        }
        
        binding.cardFeature1.setOnClickListener {
            showComingSoon("Smart Connectivity")
        }
        
        binding.cardFeature2.setOnClickListener {
            showComingSoon("Secure Platform")
        }
        
        binding.cardFeature3.setOnClickListener {
            showComingSoon("Real-time Analytics")
        }
    }
    
    private fun setupScrollEffect() {
        binding.scrollView.setOnScrollChangeListener { _, _, scrollY, _, _ ->
            // Add elevation to toolbar on scroll
            if (scrollY > 0) {
                binding.appBar.elevation = resources.getDimension(R.dimen.toolbar_elevation)
            } else {
                binding.appBar.elevation = 0f
            }
            
            // Parallax effect for hero section
            binding.heroSection.translationY = scrollY * 0.5f
        }
    }
    
    private fun showComingSoon(feature: String) {
        com.google.android.material.snackbar.Snackbar
            .make(binding.root, "$feature - Coming Soon!", com.google.android.material.snackbar.Snackbar.LENGTH_SHORT)
            .show()
    }
}
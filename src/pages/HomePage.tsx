import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shield, Eye, Zap, CheckCircle, Users, Globe, Clock } from 'lucide-react';
import Header from '../components/Header';

export default function HomePage() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6
      }
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={containerVariants}
          >
            <motion.h1 
              variants={itemVariants}
              className="text-5xl md:text-7xl font-bold text-slate-800 mb-6"
            >
              Urban Guard
            </motion.h1>
            <motion.p 
              variants={itemVariants}
              className="text-xl md:text-2xl text-slate-600 mb-8 max-w-3xl mx-auto"
            >
              Advanced AI-powered signage detection system that automatically identifies and classifies authorized and unauthorized signage in urban environments
            </motion.p>
            <motion.div 
              variants={itemVariants}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link 
                to="/signup" 
                className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-all duration-300 transform hover:scale-105"
              >
                Get Started
              </Link>
              <a 
                href="#about" 
                className="border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-600 hover:text-white transition-all duration-300"
              >
                Learn More
              </a>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={containerVariants}
            className="text-center mb-16"
          >
            <motion.h2 
              variants={itemVariants}
              className="text-4xl font-bold text-slate-800 mb-6"
            >
              About Urban Guard
            </motion.h2>
            <motion.p 
              variants={itemVariants}
              className="text-lg text-slate-600 max-w-3xl mx-auto"
            >
              Our cutting-edge AI technology revolutionizes urban signage management by providing instant, accurate classification of signage compliance
            </motion.p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Eye,
                title: "AI-Powered Detection",
                description: "Advanced computer vision algorithms that can instantly identify and analyze signage in urban environments"
              },
              {
                icon: Zap,
                title: "Real-Time Processing",
                description: "Get instant results with our optimized deep learning models that process images in seconds"
              },
              {
                icon: CheckCircle,
                title: "High Accuracy",
                description: "Our trained models achieve industry-leading accuracy in distinguishing authorized from unauthorized signage"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={itemVariants}
                whileHover={{ scale: 1.05 }}
                className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <feature.icon className="h-12 w-12 text-blue-600 mb-4" />
                <h3 className="text-xl font-semibold text-slate-800 mb-3">{feature.title}</h3>
                <p className="text-slate-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Values and Impact Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={containerVariants}
            className="text-center mb-16"
          >
            <motion.h2 
              variants={itemVariants}
              className="text-4xl font-bold text-slate-800 mb-6"
            >
              Our Values & Impact
            </motion.h2>
            <motion.p 
              variants={itemVariants}
              className="text-lg text-slate-600 max-w-3xl mx-auto"
            >
              We're building the future of urban management with innovative AI solutions
            </motion.p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {[
              {
                icon: Globe,
                title: "Innovation First",
                description: "Pioneering new technologies to solve complex urban challenges with cutting-edge AI solutions"
              },
              {
                icon: Users,
                title: "User-Centric Design",
                description: "Building intuitive tools that empower city officials and organizations to work more efficiently"
              },
              {
                icon: Clock,
                title: "Continuous Learning",
                description: "Our AI models continuously improve through advanced machine learning techniques and feedback"
              }
            ].map((value, index) => (
              <motion.div
                key={index}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={itemVariants}
                whileHover={{ scale: 1.05 }}
                className="text-center p-6"
              >
                <motion.div 
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.6 }}
                  className="inline-block mb-4"
                >
                  <value.icon className="h-16 w-16 text-blue-600" />
                </motion.div>
                <h3 className="text-xl font-semibold text-slate-800 mb-3">{value.title}</h3>
                <p className="text-slate-600">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Ready to Join Section */}
      <section className="py-20 bg-slate-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={containerVariants}
          >
            <motion.h2 
              variants={itemVariants}
              className="text-4xl font-bold text-white mb-6"
            >
              Ready to Join?
            </motion.h2>
            <motion.p 
              variants={itemVariants}
              className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto"
            >
              Start using Urban Guard today and experience the future of AI-powered signage detection
            </motion.p>
            <motion.div variants={itemVariants}>
              <Link 
                to="/signup" 
                className="bg-blue-600 text-white px-10 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-all duration-300 transform hover:scale-105 inline-block"
              >
                Ready to Join
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
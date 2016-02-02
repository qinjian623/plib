module QPlugin
  class QPlugin

    def load_plugin(path)
      require path
    end
    
    def load_plugins(dir)
      Dir.glob(dir + "/**/*.rb").each{ |p| load_plugin p}
    end
    
    
  end

  
end

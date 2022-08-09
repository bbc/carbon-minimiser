from carbon_minimiser.minimiser_api.app import app, min
import carbon_minimiser.config as CONFIG

def main(port):
    app.run(host='0.0.0.0', port=port)

min.set_cache(True, CONFIG.cache_refresh) if CONFIG.cache else min.set_cache(False)
    
port = CONFIG.port

main(port)

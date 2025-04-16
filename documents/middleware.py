class PDFSecurityMiddleware:
    """
    Middleware que modifica cabeçalhos de segurança para permitir 
    a exibição de PDFs em iframes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Se a resposta for um PDF e for para visualização inline
        if (response.get('Content-Type') == 'application/pdf' and 
            response.get('Content-Disposition', '').startswith('inline')):
            
            # Permitir que o PDF seja exibido em um iframe do mesmo domínio
            response['X-Frame-Options'] = 'SAMEORIGIN'
            response['Content-Security-Policy'] = "frame-ancestors 'self'"
            
        return response 
#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas de configuração do Gunicorn
Execute este script no servidor para verificar a configuração atual
"""

import os
import sys
from pathlib import Path

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_file_exists(filepath, description):
    """Verifica se um arquivo existe e mostra seu conteúdo"""
    print(f"\n[CHECK] {description}")
    print(f"Path: {filepath}")
    
    if os.path.exists(filepath):
        print("✅ EXISTE")
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"Tamanho: {len(content)} bytes")
                print("\n--- CONTEÚDO ---")
                print(content)
                print("--- FIM ---")
            except Exception as e:
                print(f"❌ Erro ao ler arquivo: {e}")
    else:
        print("❌ NÃO EXISTE (correto se for wsgi.py na raiz)")

def main():
    print_section("DIAGNÓSTICO DO SERVIDOR - STATSFUT.COM")
    
    # Diretório base
    base_dir = Path(__file__).resolve().parent
    print(f"\nDiretório base: {base_dir}")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    print_section("1. VERIFICANDO ARQUIVOS CRÍTICOS")
    
    # Verificar wsgi.py na raiz (NÃO deveria existir)
    check_file_exists(
        base_dir / "wsgi.py",
        "wsgi.py na RAIZ (NÃO deveria existir!)"
    )
    
    # Verificar core/wsgi.py (DEVE existir)
    check_file_exists(
        base_dir / "core" / "wsgi.py",
        "core/wsgi.py (DEVE existir)"
    )
    
    # Verificar gunicorn.conf
    check_file_exists(
        base_dir / "gunicorn.conf",
        "gunicorn.conf"
    )
    
    # Verificar core/settings.py
    check_file_exists(
        base_dir / "core" / "settings.py",
        "core/settings.py"
    )
    
    print_section("2. VERIFICANDO VARIÁVEIS DE AMBIENTE")
    
    django_settings = os.environ.get('DJANGO_SETTINGS_MODULE', 'NÃO DEFINIDA')
    print(f"DJANGO_SETTINGS_MODULE: {django_settings}")
    
    print_section("3. TESTANDO IMPORTAÇÃO DO WSGI")
    
    # Adicionar o diretório base ao path
    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))
        print(f"✅ Adicionado {base_dir} ao sys.path")
    
    print(f"\nsys.path atual:")
    for i, p in enumerate(sys.path[:5]):
        print(f"  {i}: {p}")
    
    # Tentar importar core.wsgi
    print("\n[TEST] Tentando importar core.wsgi.application...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        from core.wsgi import application
        print("✅ SUCESSO! core.wsgi.application importado corretamente")
        print(f"   Tipo: {type(application)}")
    except Exception as e:
        print(f"❌ ERRO ao importar: {e}")
        import traceback
        traceback.print_exc()
    
    print_section("4. LISTANDO ARQUIVOS NO DIRETÓRIO RAIZ")
    
    files = sorted(os.listdir(base_dir))
    print("\nArquivos e diretórios na raiz:")
    for item in files[:20]:  # Primeiros 20 itens
        path = base_dir / item
        if os.path.isdir(path):
            print(f"  📁 {item}/")
        else:
            size = os.path.getsize(path)
            print(f"  📄 {item} ({size} bytes)")
    
    print_section("5. RESUMO E RECOMENDAÇÕES")
    
    wsgi_root = base_dir / "wsgi.py"
    wsgi_core = base_dir / "core" / "wsgi.py"
    gunicorn_conf = base_dir / "gunicorn.conf"
    
    issues = []
    
    if os.path.exists(wsgi_root):
        issues.append("❌ PROBLEMA: wsgi.py existe na raiz - DEVE SER DELETADO!")
    else:
        print("✅ wsgi.py NÃO existe na raiz (correto)")
    
    if not os.path.exists(wsgi_core):
        issues.append("❌ PROBLEMA: core/wsgi.py NÃO existe - DEVE EXISTIR!")
    else:
        print("✅ core/wsgi.py existe (correto)")
    
    if os.path.exists(gunicorn_conf):
        with open(gunicorn_conf, 'r') as f:
            conf_content = f.read()
            if 'wsgi-app' in conf_content or 'wsgi_app' in conf_content:
                issues.append("❌ PROBLEMA: gunicorn.conf contém 'wsgi-app' - DEVE SER REMOVIDO!")
            else:
                print("✅ gunicorn.conf NÃO contém wsgi-app (correto)")
    
    if issues:
        print("\n⚠️  PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ Nenhum problema de configuração encontrado!")
        print("   Se ainda houver erro, pode ser problema de permissões ou cache.")
    
    print("\n" + "="*60)
    print("Diagnóstico concluído!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

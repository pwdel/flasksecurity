"""Compile static assets."""
from flask_assets import Bundle

def compile_static_assets(assets):
    """Configure and build asset bundles."""

    # Main asset bundles
    main_style_bundle = Bundle(
        filters='cssmin',
        output='dist/css/landing.css',
        extra={'rel': 'stylesheet/css'}
    )
    main_js_bundle = Bundle(
        'src/js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js'
    )

    # Admin asset bundleds
    admin_style_bundle = Bundle(
        filters='cssmin',
        output='dist/css/account.css',
        extra={'rel': 'stylesheet/css'}
    )
    assets.register('main_styles', main_style_bundle)
    assets.register('main_js', main_js_bundle)
    assets.register('admin_styles', admin_style_bundle)
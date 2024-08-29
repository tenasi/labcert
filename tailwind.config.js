/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./labcert/templates/**/*.html",
        "./labcert/static/src/**/*.js",
        "./node_modules/flowbite/**/*.js"
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                primary: { "50": "#eff6ff", "100": "#dbeafe", "200": "#bfdbfe", "300": "#93c5fd", "400": "#60a5fa", "500": "#3b82f6", "600": "#007bff", "700": "#1d4ed8", "800": "#1e40af", "900": "#1e3a8a" }
            }
        },
        fontFamily: {
            'body': [
                'Montserrat'
            ],
            'sans': [
                'Montserrat'
            ],
        },
    },
    plugins: [
        require('flowbite/plugin')
    ],
}

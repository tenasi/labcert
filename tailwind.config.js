/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./labcert/templates/**/*.html",
        "./labcert/static/src/**/*.js",
        "./node_modules/flowbite/**/*.js"
    ],
    safelist: [
        "pl-4",
        "pl-8",
        "pl-12",
        "pl-16",
        "pl-20",
        "pl-24",
        "pl-28",
        "pl-32",
        "pl-36",
        "pl-40",
        "pl-44",
        "pl-48",
        "pl-52",
        "pl-56",
        "pl-60",
        "pl-64",
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

from .models import Provincia, Municipio


def poblar_provincias():
    provincias = [
        'Pinar del Río', 'Artemisa', 'La Habana', 'Mayabeque', 'Matanzas',
        'Cienfuegos', 'Villa Clara', 'Sancti Spíritus', 'Ciego de Ávila',
        'Camagüey', 'Las Tunas', 'Holguín', 'Granma', 'Santiago de Cuba',
        'Guantánamo', 'Isla de la Juventud'
    ]

    for provincia_nombre in provincias:
        Provincia.objects.get_or_create(nombre=provincia_nombre)


def poblar_municipios():
    municipios_por_provincia = {
        'Pinar del Río': [
            'Pinar del Río', 'Viñales', 'La Palma', 'San Luis', 'Los Palacios',
            'Mantua', 'Candelaria', 'Bahía Honda', 'Sandino', 'Guane'
        ],
        'Artemisa': [
            'Artemisa', 'Mariel', 'Guanajay', 'San Antonio de los Baños',
            'Bauta', 'Caimito', 'Las Cruces', 'Santo Domingo'
        ],
        'La Habana': [
            'La Habana', 'Habana del Este', 'La Lisa', 'Regla', 'Boyeros',
            'Centro Habana', 'Playa', 'Cerro', 'Diez de Octubre', 'San Miguel del Padrón',
            'La Habana Vieja'
        ],
        'Mayabeque': [
            'Güines', 'Melena del Sur', 'San José de las Lajas',
            'Arroyo Naranjo', 'Jaruco', 'Santiago de las Vegas', 'San Nicolás'
        ],
        'Matanzas': [
            'Matanzas', 'Varadero', 'Cárdenas', 'Colón', 'Jagüey Grande',
            'Los Arabos', 'Limonar', 'Martí', 'Perico', 'Unión de Reyes'
        ],
        'Cienfuegos': [
            'Cienfuegos', 'Aguada de Pasajeros', 'Abreus', 'Rodas',
            'Palmira', 'Lajas', 'Cruces', 'Cumanayagua'
        ],
        'Villa Clara': [
            'Santa Clara', 'Sagua la Grande', 'Remedios', 'Camajuaní',
            'Corralillo', 'Caibarién', 'Encrucijada', 'Cifuentes',
            'Manicaragua', 'Placetas'
        ],
        'Sancti Spíritus': [
            'Sancti Spíritus', 'Trinidad', 'Yaguajay', 'Fomento',
            'Cabaiguán', 'La Sierpe', 'Taguasco', 'Jatibonico'
        ],
        'Ciego de Ávila': [
            'Ciego de Ávila', 'Morón', 'Chambas',
            'Majagua', 'Bolivia', 'Baraguá', 'Ciro Redondo', 'Florencia', 'Primero de Enero', 'Venezuela'
        ],
        'Camagüey': [
            'Camagüey', 'Florida', 'Nuevitas', 'Esmeralda',
            'Sierra de Cubitas', 'Jimaguayú', 'Guáimaro', 'Najasa', 'Vertientes', 'Minas', 'Santa Cruz del Sur'
        ],
        'Las Tunas': [
            'Las Tunas', 'Manatí', 'Colombia', 'Majibacoa',
            'Jobabo', 'Jesús Menéndez', 'Puerto Padre', 'Amancio'
        ],
        'Holguín': [
            'Holguín', 'Banes', 'Antilla', 'Báguanos',
            'Cacocum', 'Calixto García', 'Cueto', 'Frank País', 'Gibara', 'Mayarí', 'Moa', 'Rafael Freyre',
            'Sagua de Tánamo', 'Urbano Noris'
        ],
        'Granma': [
            'Bayamo', 'Manzanillo', 'Yara', 'Media Luna',
            'Niquero', 'Pilón', 'Jiguaní', 'Buey Arriba',
            'Bartolomé Masó', 'Campechuela', 'Cauto Cristo', 'Guisa', 'Río Cauto'
        ],
        'Santiago de Cuba': [
            'Santiago de Cuba', 'Segundo Frente', 'Tercer Frente',
            'San Luis', 'Contramaestre', 'Palma Soriano',
            'Songo-La Maya', 'Mella'
        ],
        'Guantánamo': [
            'Guantánamo', 'Baracoa', 'Maisí', 'Manuel Tames',
            'Yateras', 'San Antonio del Sur', 'El Salvador',
            'Niceto Pérez', 'Caimanera', 'Imías'
        ],
        'Isla de la Juventud': [
            'Isla de la Juventud'
        ],
    }

    for provincia_nombre, municipios in municipios_por_provincia.items():
        provincia = Provincia.objects.get(nombre=provincia_nombre)
        for municipio_nombre in municipios:
            Municipio.objects.create(nombre=municipio_nombre, provincia=provincia)


poblar_provincias()
poblar_municipios()

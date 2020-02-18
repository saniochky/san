import folium
import folium.plugins
import googlemaps
from math import sin, cos, sqrt, atan2, radians


def read(name, year, country):
    '''
    Reads a list of movies and location where they have been created
    and returns a set of locations.
    :param name: str
    :param year: int
    :param country: str
    :return: set
    >>> read('locations.list' ,1888)
    {'England, UK', 'Hannover, Lower Saxony, Germany',
    'West Yorkshire, England, UK',
    'Leeds, West Yorkshire, England, UK',
    'Roundhay, Leeds, West Yorkshire, England, UK', 'UK'}
    '''
    lst = set([])
    year = '(' + str(year) + ')'
    f = open(name, 'r')
    for line in f.readlines():
        line = line.strip().lower()
        line = line.split()
        if year in line:
            if country in line:
                line = ' '.join(line)
                if '{' in line:
                    line = line[0:line.index('{')] + line[line.index('}')+1:]
                line = line.split()
                if '()' in line:
                    line.remove('()')
                if year in line:
                    line = line[line.index(year)+1:]
                    line = ' '.join(line)
                    while '(' in line and ')' in line:
                        line = line[0:line.index('(')] + line[line.index(')')+1:]
                    line = line.split()
                    line = ' '.join(line)
                    lst.add(line)
    f.close()
    return lst


def coordinates(lst):
    '''
    Returns set of tuples of coordinates of given set of locations.
    :param lst: set
    :return: set
    >>> coordinates({'Kiev'})
    {(50.4501, 30.5234)}
    >>> coordinates({'London', 'Miami'})
    {(51.5073509, -0.1277583), (25.7616798, -80.1917902)}
    '''
    coo_lst = set([])
    gmaps = googlemaps.Client(key='AIzaSyALtNqb4VsrQbkkA9HqBvJ3r7NWAEYtXgM')
    for el in lst:
        error = 0
        try:
            location = gmaps.geocode(el)
        except googlemaps.exceptions.HTTPError:
            pass
            error = 1
        if error == 0:
            if location:
                coo_lst.add((location[0]['geometry']['location']['lat'],
                             location[0]['geometry']['location']['lng']))
    return coo_lst


def address(lat, lng):
    '''
    Returns address of place with given latitude and longitude.
    :param lat: float
    :param lng: float
    :return: str
    >>> address(40.714224, -73.961452)
    '279 Bedford Ave, Brooklyn, NY 11211, USA'
    >>> address(49.8176362, 24.0230669)
    "Kozelnytska St, 4, L'viv, L'vivs'ka oblast, Ukraine, 79000"
    '''
    gmaps = googlemaps.Client(key='AIzaSyALtNqb4VsrQbkkA9HqBvJ3r7NWAEYtXgM')
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    return reverse_geocode_result[0]['formatted_address']


def distance(lat1, lng1, lat2, lng2):
    '''
    Returns distance between 2 places with given latitude and longitude in km.
    :param lat1: float
    :param lng1: float
    :param lat2: float
    :param lng2: float
    :return: float
    >>> distance(51.5073509, -0.1277583, 25.7616798, -80.1917902)
    7129.132
    >>> distance(50.4501, 30.5234, -33.865143, 151.209900)
    14947.847
    '''
    Radius = 6373.0

    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    dlng = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    dstnc = Radius * c
    return round(dstnc, 3)


def create(lat, lng, lst, maxx):
    '''
    Creates a map using folium.
    :param lat: float
    :param lng: float
    :param lst: set
    :param maxx: int
    :return: None
    '''
    index = 0
    global dst
    dst = {}
    map = folium.Map(location=[lat, lng], zoom_start=12)
    tooltip = 'Click me!'
    for el in lst:
        if distance(lat, lng, el[0], el[1]) < maxx:
            dst[distance(lat, lng, el[0], el[1])] = el
    dst = dict(sorted(dst.items()))
    folium.Marker([lat, lng],
                  popup=address(lat, lng),
                  tooltip='My location',
                  icon=folium.Icon(color='red')).add_to(map)
    for key in dst:
        if dst[key][0] != lat and dst[key][1] != lng:
            folium.Marker([dst[key][0], dst[key][1]],
                          popup=address(dst[key][0], dst[key][1]),
                          tooltip=tooltip,
                          icon=folium.Icon(
                              color='blue',
                              icon='info-sign'
                          )).add_to(map)
            if index > 9:
                break
            index += 1
    index = 0
    for key in dst:
        if dst[key][0] != lat and dst[key][1] != lng:
            line_object = folium.PolyLine([(lat, lng), dst[key]],
                                          color='#f533ff',
                                          weight=6,
                                          tooltip=str(int(key)) + ' kilometers')
            line_object.add_to(map)
            folium.plugins.PolyLineTextPath(line_object,
                                            text=str(int(key)) +
                                            ' kilometers' + ' '*5,
                                            color='blue',
                                            repeat=True,
                                            center=True).add_to(map)
            if index > 9:
                break
            index += 1
    map.save(str(year) + '_movies_map.html')
    return None


def main():
    '''
    Main function that uses all other functions and
    interacts with the user.
    :return: None
    '''
    global year
    year = int(input('Please enter a year you would like to have a map for: '))
    location = input('Please enter your location (format: lat, long): ')
    maxx = 601
    if ', ' in location:
        lat, lng = float(
            location.split(', ')[0]), float(location.split(', ')[1])
        country = address(lat, lng).split(', ')
        if not country[-1].isdigit():
            country = country[-1].lower()
        else:
            country = country[-2].lower()
        print('Starting...')
        loc_list = read('locations.list', year, country)
        if loc_list:
            print('Please wait...')
            loc_list = coordinates(loc_list)
            print('Map is generating...')
            create(lat, lng, loc_list, maxx)
            if not dst:
                create(lat, lng, loc_list, maxx * 2)
            if not dst:
                print(
                    'There is not any place where films',
                    'were filmed in this country this year.'
                    )
            else:
                print(
                    'Finished. Please have a look at the map ' +
                    str(year) + '_movies_map.html'
                )
        else:
            print('This year is not in the list.')
    else:
        print('Invalid value. Please write coordinates in format: lat, long.')
    return None


if __name__ == "__main__":
    main()

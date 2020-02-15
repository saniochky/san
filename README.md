# Filming map
Filming map is a Python module that allows demonstrating places where films were filmed.

## Detailed information
Filming map uses locations.list from imdb.com, folium, and googlemaps libraries.
It requires location (in format: lat, lng) and year. 
Than an html map is created.
It might take quite a bit of time because of an enormous amount of information about films.
But the most time is wasted when the module takes information from Google maps, and I can not deal with it.

## Map itself
The map has three layers

First layer:
The map itself

Second layer:
Markers
A red marker which shows your position (or position which you specified).
Ten or fewer blue markers which show 10 or less nearest places where films were filmed.
If you point your mouse on a blue marker, you will see 'Click me!' message.
When you click on it, you will see an accurate address of the place.
The red marker also shows an accurate address of your position.

Third layer:
Distance
The red marker is connected with every blue marker with purple lines.
On every purple line, there is a text where the distance between the red and blue marker is specified.
If you point your mouse on any line, you will also see a message about distance.

## Errors
If your location is written in the wrong format, you will this message:
```python
'Invalid value. Please write coordinates in format: lat, long.'
```
If there is not any information about a specified year in the list, you will see this message
```python
'This year is not in the list'
```
If there is not any places where films were filmed, you will see this message: 
```python
'There is not any place where films, were created in this region this year.'
```
If any other problems occur, please inform the developer, and he will try to fix them.

## Example
```python
main.py
Please enter a year you would like to have a map for: 1896
Please enter your location (format: lat, long): 52.520008, 13.404954
Starting...
Please wait...
Map is generating...
Finished. Please have a look at the map 1913_movies_map.html
```
1913_movies_map.html
![Screenshot of map](https://1drv.ms/u/s!AoUAS1XAhyZZjGwfG9YPg09stOZT)

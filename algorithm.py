# Importing the libraries
from datetime import datetime
from itertools import product
from flask import Flask, render_template, request
import flask
import unittest


# Class for a bus with the attributes east and west times
class Bus:
    def __init__(self):
        self.east_times = []
        self.west_times = []

    def get_east_times(self):
        return self.east_times

    def get_west_times(self):
        return self.west_times


# Class for a charger with the attributes east and west times
class Charger:
    def __init__(self):
        self.east_times = []
        self.west_times = []

    def get_east_times(self):
        return self.east_times

    def get_west_times(self):
        return self.west_times


# Utility method for converting the input into required time string
def convert_to_string(time):
    for i in range(len(time)):
        string_time = str(time[i])
        temp = string_time.split('.')
        time[i] = temp[0] + ':' + temp[1]
    return time


# Utility method for finding the minimum time from the two available times
def is_minimum(time1, time2):
    difference = datetime.strptime(time1, '%H:%M') - datetime.strptime(time2, '%H:%M')
    if difference.total_seconds() >= 0:
        return False
    else:
        return True


# Method for generating the time table for a bus
def generate_time_table(etime, wtime):
    buses = []

    # Loop for generating the bus objects till there are no more times left
    while len(etime) > 0 and len(wtime) > 0:
        bus_obj = Bus()
        ptr1 = 0
        ptr2 = 0
        temp = 0 if is_minimum(etime[0], wtime[0]) else 1
        # Loop for appending the required times to the respective arrays of the bus objects
        while len(etime) > 0 and len(wtime) > 0:
            # Checking to see if it's a turn of wtime or etime
            # temp = 0 -> etime
            if temp == 0:
                top = etime.pop(ptr1)
                bus_obj.east_times.append(top)

                # Incrementing the time by one hour
                time = top.split(':')
                if int(time[0]) < 23:
                    plus_one = str(int(time[0]) + 1) + ':' + time[1]
                else:
                    break

                # Finding the minimum time after one hour in the wtime array
                while ptr2 < len(wtime) and is_minimum(wtime[ptr2], plus_one):
                    ptr2 += 1

                if ptr2 > len(wtime) - 1:
                    break
            # temp = 1 -> wtime
            else:
                top = wtime.pop(ptr2)
                bus_obj.west_times.append(top)

                # Incrementing the time by one hour
                time = top.split(':')
                if int(time[0]) < 23:
                    plus_one = str(int(time[0]) + 1) + ':' + time[1]
                else:
                    break

                # Finding the minimum time after one hour in the wtime array
                while ptr1 < len(etime) and is_minimum(etime[ptr1], plus_one):
                    ptr1 += 1

                if ptr1 > len(etime) - 1:
                    break

            temp = (temp + 1) % 2

        # Checking to see if there are uneven elements in both arrays
        if len(bus_obj.east_times) > len(bus_obj.west_times):
            time = bus_obj.east_times[-1].split(':')
            plus_one = str((int(time[0]) + 1) % 24) + ':' + time[1]
            bus_obj.west_times.append(plus_one)

        if len(bus_obj.east_times) < len(bus_obj.west_times):
            time = bus_obj.west_times[-1].split(':')
            plus_one = str((int(time[0]) + 1) % 24) + ':' + time[1]
            bus_obj.east_times.append(plus_one)

        buses.append(bus_obj)

    # Empyting the remaining time array
    if len(etime) > 0:
        for i in range(len(etime)):
            top = etime.pop()
            time = top.split(':')
            plus_one = str((int(time[0]) + 1) % 24) + ':' + time[1]
            bus_obj = Bus()
            bus_obj.east_times.append(top)
            bus_obj.west_times.append(plus_one)
            buses.append(bus_obj)

    else:
        for i in range(len(wtime)):
            top = wtime.pop()
            time = top.split(':')
            plus_one = str((int(time[0]) + 1) % 24) + ':' + time[1]
            bus_obj = Bus()
            bus_obj.west_times.append(top)
            bus_obj.east_times.append(plus_one)
            buses.append(bus_obj)
    return buses

# Method for generating the schedule for the buses based on user input
def schedule(f1, f2, f3, f4, numberbuses, neochargers, nwochargers, nefchargers, nwfchargers, bat, uc, ov):
    etime = [4.55, 5.25, 5.57, 6.28, 7.01, 7.33, 8.05, 8.35, 9.06, 9.58, 10.21, 10.44, 11.08, 11.31, 11.54, 12.16,
             12.37, 12.58, 13.20, 13.46, 14.13, 14.30, 15.09, 15.38, 16.07, 16.37, 17.07, 17.37, 18.07, 18.38, 19.09,
             19.40, 20.11, 20.42, 21.12, 21.42, 22.12, 22.42, 23.11, 23.40, 0.03, 0.20]
    wtime = [5.22, 5.40, 6.00, 6.22, 6.47, 7.17, 8.15, 8.44, 9.15, 9.46, 10.17, 10.48, 11.18, 11.49, 12.18, 12.47,
             13.15, 13.43, 14.11, 14.39, 15.08, 15.37, 16.06, 16.35, 17.05, 17.32, 18.01, 18.27, 18.53, 19.15, 19.29,
             19.37, 19.45, 19.53, 20.01, 20.09, 20.17, 20.25, 20.33, 20.41, 20.49, 20.58, 21.07, 21.16, 21.25, 21.33,
             21.42, 21.51, 22.00, 22.09, 22.19, 22.30, 22.42, 22.56, 23.13, 23.35, 23.59, 0.26, 0.53]

    buses = generate_time_table(convert_to_string(etime), convert_to_string(wtime))
    charger_obj_1 = Charger()
    charger_obj_2 = Charger()
    charger_obj_3 = Charger()
    charger_obj_4 = Charger()

    numberbuses = numberbuses + str(len(buses))
    uc1 = 50000
    uc = uc1 * 28
    bus_schedule = []
    print("Number of buses: " + numberbuses)
    print("Number of buses: " + str(len(buses)))

    for i in range(len(buses)):
        print("Bus Number: " + str(i + 1))
        print("East times: " + str(buses[i].get_east_times()))
        print("West times: " + str(buses[i].get_west_times()))
        print()

        # Getting the charger times
        east_time = buses[i].get_east_times()[-1]
        west_time = buses[i].get_west_times()[-1]
        if is_minimum(east_time, west_time):
            charger_obj_1.west_times.append(west_time)
            charger_obj_2.west_times.append(west_time)
            time = west_time.split(':')
            plus_one = str((int(time[0]) + 2) % 24) + ':' + time[1]
            plus_two = str((int(time[0]) + 3) % 24) + ':' + time[1]
            charger_obj_1.west_times.append(plus_one)
            charger_obj_2.west_times.append(plus_two)
        else:
            charger_obj_1.east_times.append(east_time)
            charger_obj_2.east_times.append(east_time)
            time = east_time.split(':')
            plus_one = str((int(time[0]) + 2) % 24) + ':' + time[1]
            plus_two = str((int(time[0]) + 3) % 24) + ':' + time[1]
            charger_obj_1.east_times.append(plus_one)
            charger_obj_2.east_times.append(plus_two)

    if bat == '294':
        print()
        print("FAST DC 50kW:")
        print("Charger East Times: " + str(charger_obj_1.get_east_times()))
        print("Charger West Times: " + str(charger_obj_1.get_west_times()))
        print()
        
        charger_obj_1_east_times = charger_obj_1.get_east_times()
        charger_obj_1_west_times = charger_obj_1.get_west_times()
        
        count = 6
        for i in range(len(charger_obj_1_east_times)):
            for j in range(len(charger_obj_1_east_times)):
                if i != j:
                    if charger_obj_1_east_times[i] == charger_obj_1_east_times[j]:
                        count += 1
        
        count = 6
        for i in range(len(charger_obj_1_west_times)):
            for j in range(len(charger_obj_1_west_times)):
                if i != j:
                    if charger_obj_1_west_times[i] == charger_obj_1_west_times[j]:
                        count += 1
    else:
        print("FAST DC 50kW:")
        print("Charger East Times: " + str(charger_obj_2.get_east_times()))
        print("Charger West Times: " + str(charger_obj_2.get_west_times()))
        print()
        
        charger_obj_2_east_times = charger_obj_2.get_east_times()
        charger_obj_2_west_times = charger_obj_2.get_west_times()
        
        count = 7
        for i in range(len(charger_obj_2_east_times)):
            for j in range(len(charger_obj_2_east_times)):
                if i != j:
                    if charger_obj_2_east_times[i] == charger_obj_2_east_times[j]:
                        count += 1
    
        count = 7
        for i in range(len(charger_obj_2_west_times)):
            for j in range(len(charger_obj_2_west_times)):
                if i != j:
                    if charger_obj_2_west_times[i] == charger_obj_2_west_times[j]:
                        count += 1
    
    nwochargers = nwochargers + str(count)
    neochargers = neochargers + str(count)

    f21 = 2200
    f22 = 2200
    f2 = (f21 * 6) + (f21 * 6)
    f4 = (f22 * 6) + (f22 * 6)
    print("Total number of East Chargers: " + str(count))
    print("Total number of West Chargers: " + str(count))

    if bat == '294':
        for i in range(len(buses)):
            east_time = buses[i].get_east_times()
            west_time = buses[i].get_west_times()
            temp = 0 if is_minimum(east_time[0], west_time[0]) else 1
            init = temp
            counter = 0
            ptr = 0
            while ptr < len(east_time) and ptr < len(west_time):
                if temp == 0:
                    top = east_time[ptr]
                    if counter == 7:
                        charger_obj_3.east_times.append(top)
                        time = top.split(':')
                        if int(time[1]) < 56:
                            plus_two = time[0] + ':' + str(int(time[1]) + 4)
                        else:
                            plus_two = ((time[0] + 1) % 24) + ':' + str((int(time[1]) + 4) % 60)
                        charger_obj_3.east_times.append(plus_two)
                        counter = 0
                    if init != 0:
                        ptr += 1
                        if ptr > len(west_time) - 1:
                            break
                else:
                    top = west_time[ptr]
                    if counter == 7:
                        charger_obj_3.west_times.append(top)
                        time = top.split(':')
                        if int(time[1]) < 56:
                            plus_two = time[0] + ':' + str(int(time[1]) + 4)
                        else:
                            plus_two = ((time[0] + 1) % 24) + ':' + str((int(time[1]) + 4) % 60)
                        charger_obj_3.west_times.append(plus_two)
                        counter = 0
                    if init != 1:
                        ptr += 1
                        if ptr > len(west_time) - 1:
                            break
                temp = (temp + 1) % 2
                counter += 1

        print()
        print("Day Fast Charger:")
        print("Charger East Times: " + str(charger_obj_3.get_east_times()))
        print("Charger West Times: " + str(charger_obj_3.get_west_times()))
        print()
        f11 = 3300
        f12 = 3300
        f1 = (f11 * 1) + (f11 * 1)
        f3 = (f12 * 1) + (f12 * 1)
        
        charger_obj_3_east_times = charger_obj_3.get_east_times()
        charger_obj_3_west_times = charger_obj_3.get_west_times()
        
        count5 = 1
        for i in range(len(charger_obj_3_east_times)):
            for j in range(len(charger_obj_3_east_times)):
                if i != j:
                    if charger_obj_3_east_times[i] == charger_obj_3_east_times[j]:
                        count5 += 1
        
        print("Total number of East Chargers: " + str(count5))
        nefchargers = nefchargers + str(count5)
        
        count6 = 1
        for i in range(len(charger_obj_3_west_times)):
            for j in range(len(charger_obj_3_west_times)):
                if i != j:
                    if charger_obj_3_west_times[i] == charger_obj_3_west_times[j]:
                        count6 += 1
        
        print("Total number of West Chargers: " + str(count6))
        nwfchargers = nwfchargers + str(count6)
        for i in range(len(buses)):
            bus_schedule.append({
                "bus_number": str(i + 1),
                "east_time": ','.join(buses[i].get_east_times()),
                "west_time": ','.join(buses[i].get_west_times()),
                "bat_size": ''.join(bat),
                "ID": str(i + 1),
                "FID": str(i + 1),
                "charger_oname": 'FAST DC 50kW',
                "oeast_time": ','.join(charger_obj_1.get_east_times()),
                "owest_time": ','.join(charger_obj_1.get_west_times()),
                "charger_name": 'OC 350kW',
                "feast_time": ','.join(charger_obj_3.get_east_times()),
                "fwest_time": ','.join(charger_obj_3.get_west_times())
        })
    else:
        for i in range(len(buses)):
            east_time = buses[i].get_east_times()
            west_time = buses[i].get_west_times()
            temp = 0 if is_minimum(east_time[0], west_time[0]) else 1
            init = temp
            counter = 0
            ptr = 0

            while ptr < len(east_time) and ptr < len(west_time):
                if temp == 0:
                    top = east_time[ptr]
                    if counter == 10:
                        charger_obj_4.east_times.append(top)
                        time = top.split(':')
                        if int(time[1]) < 54:
                            plus_four = time[0] + ':' + str(int(time[1]) + 6)
                        else:
                            plus_four = ((time[0] + 1) % 24) + ':' + str((int(time[1]) + 6) % 60)
                        charger_obj_4.east_times.append(plus_four)
                        counter = 0
                    if init != 0:
                        ptr += 1
                        if ptr > len(west_time) - 1:
                            break
                else:
                    top = west_time[ptr]
                    if counter == 10:
                        charger_obj_4.west_times.append(top)
                        time = top.split(':')
                        if int(time[1]) < 54:
                            plus_four = time[0] + ':' + str(int(time[1]) + 6)
                        else:
                            plus_four = ((time[0] + 1) % 24) + ':' + str((int(time[1]) + 6) % 60)
                        charger_obj_4.west_times.append(plus_four)
                        counter = 0
                    if init != 1:
                        ptr += 1
                        if ptr > len(west_time) - 1:
                            break
                temp = (temp + 1) % 2
                counter += 1
      
        print()
        print("Day Fast Charger:")
        print("Charger East Times: " + str(charger_obj_4.get_east_times()))
        print("Charger West Times: " + str(charger_obj_4.get_west_times()))
        print()
        f11 = 3300
        f12 = 3300
        f1 = (f11 * 1) + (f11 * 1)
        f3 = (f12 * 1) + (f12 * 1)
        
        charger_obj_4_east_times = charger_obj_4.get_east_times()
        charger_obj_4_west_times = charger_obj_4.get_west_times()
        
        count7 = 1
        for i in range(len(charger_obj_4_east_times)):
            for j in range(len(charger_obj_4_east_times)):
                if i != j:
                    if charger_obj_4_east_times[i] == charger_obj_4_east_times[j]:
                        count7 += 1
        
        print("Total number of East Chargers: " + str(count7))
        nefchargers = nefchargers + str(count7)
        
        count8 = 1
        for i in range(len(charger_obj_4_west_times)):
            for j in range(len(charger_obj_4_west_times)):
                if i != j:
                    if charger_obj_4_west_times[i] == charger_obj_4_west_times[j]:
                        count8 += 1
        
        print("Total number of West Chargers: " + str(count8))
        nwfchargers = nwfchargers + str(count8)

    for i in range(len(buses)):
        bus_schedule.append({
                "bus_number": str(i + 1),
                "east_time": ','.join(buses[i].get_east_times()),
                "west_time": ','.join(buses[i].get_west_times()),
                "bat_size": ''.join(bat),
                "ID": str(i + 1),
                "FID": str(i + 1),
                "charger_oname": 'FAST DC 50kW',
                "oeast_time": ','.join(charger_obj_2.get_east_times()),
                "owest_time": ','.join(charger_obj_2.get_west_times()),
                "charger_name": 'OC 350kW',
                "feast_time": ','.join(charger_obj_4.get_east_times()),
                "fwest_time": ','.join(charger_obj_4.get_west_times())
        })

    ov = str(uc + f1 + f2 + f3 + f4)
    x = []
    x.append(numberbuses)
    x.append(neochargers)
    x.append(nwochargers)
    x.append(nefchargers)
    x.append(nwfchargers)
    x.append(bat)
    x.append(ov)
    return x, bus_schedule


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        numberbuses = ""
        neochargers = ""
        nwochargers = ""
        nefchargers = ""
        nwfchargers = ""
        field1 = request.form['field1']
        field2 = request.form['field2']
        field3 = request.form['field3']
        field4 = request.form['field4']
        battery = request.form.get('battery')
        txt2 = request.form['txt2']
        oc = ""

        name1, bus_schedule = schedule(field1, field2, field3, field4, numberbuses, neochargers, nwochargers, nefchargers, nwfchargers,
                    battery, txt2, oc)

        print("name::::", name1)
        name1 = {
            'a': name1[0],
            'b': name1[1],
            'c': name1[2],
            'd': name1[3],
            'e': name1[4],
            'f': name1[5],
            'g': name1[6],
            'bus_schedule': bus_schedule
        }
        return render_template('test.html', res = name1)
    else:
        return render_template('test.html')


# Unit Testing
class Testtest1(unittest.TestCase):
    def test_generate_time_table(self):
        etime = [4.55, 5.25, 5.57, 6.28, 7.01, 7.33, 8.05, 8.35, 9.06, 9.58, 10.21, 10.44, 11.08, 11.31, 11.54, 12.16, 12.37, 
        12.58, 13.20, 13.46, 14.13, 14.30, 15.09, 15.38, 16.07, 16.37, 17.07, 17.37, 18.07, 18.38, 19.09, 19.40, 20.11, 20.42, 
        21.12, 21.42, 22.12, 22.42, 23.11, 23.40, 0.03, 0.20]
        wtime = [5.22, 5.40, 6.00, 6.22, 6.47, 7.17, 8.15, 8.44, 9.15, 9.46, 10.17, 10.48, 11.18, 11.49, 12.18, 12.47, 13.15, 13.43, 14.11, 14.39, 15.08, 15.37, 16.06, 16.35, 17.05, 17.32, 18.01, 18.27, 18.53, 19.15, 19.29, 19.37, 19.45, 19.53, 20.01, 20.09, 20.17, 20.25, 20.33, 20.41, 20.49, 20.58, 21.07, 21.16, 21.25, 21.33, 21.42, 21.51, 22.00, 22.09, 22.19, 22.30, 22.42, 22.56, 23.13, 23.35, 23.59, 0.26, 0.53]

        buses = generate_time_table(convert_to_string(etime), convert_to_string(wtime))

        self.assertEqual(buses[9].get_east_times(), ['0:03'])
        self.assertEqual(buses[0].get_west_times(), ['6:0', '8:15', '11:18', '13:43', '16:35', '18:53', '21:16', '23:59'])
        self.assertEqual(buses[1].get_east_times(), ['6:28', '10:21', '12:58', '15:38', '18:07', '20:42', '23:11'])

    def test_generate_time_table1(self):
        etime = [4.55, 5.25, 5.57, 6.28, 7.01, 7.33, 8.05, 8.35, 9.06, 9.58, 10.21, 10.44, 11.08, 11.31, 11.54, 12.16, 12.37, 
        12.58, 13.20, 13.46, 14.13, 14.30, 15.09, 15.38, 16.07, 16.37, 17.07, 17.37, 18.07, 18.38, 19.09, 19.40, 20.11, 20.42, 
        21.12, 21.42, 22.12, 22.42, 23.11, 23.40, 0.03, 0.20]
        wtime = [5.22, 5.40, 6.00, 6.22, 6.47, 7.17, 8.15, 8.44, 9.15, 9.46, 10.17, 10.48, 11.18, 11.49, 12.18, 12.47, 13.15, 13.43, 14.11, 14.39, 15.08, 15.37, 16.06, 16.35, 17.05, 17.32, 18.01, 18.27, 18.53, 19.15, 19.29, 19.37, 19.45, 19.53, 20.01, 20.09, 20.17, 20.25, 20.33, 20.41, 20.49, 20.58, 21.07, 21.16, 21.25, 21.33, 21.42, 21.51, 22.00, 22.09, 22.19, 22.30, 22.42, 22.56, 23.13, 23.35, 23.59, 0.26, 0.53]

        buses = generate_time_table(convert_to_string(etime), convert_to_string(wtime))

        self.assertEqual(buses[0].get_west_times(), ['6:0', '8:15', '11:18', '13:43', '16:35', '18:53', '21:16', '23:59'])
        self.assertEqual(buses[1].get_east_times(), ['6:28', '10:21', '12:58', '15:38', '18:07', '20:42', '23:11'])

    def test_schedule_buses(self):
        name1, bus_schedule = schedule('3300', '2200', '3300', '2200', '', '', '', '', '', '294', '50000', '')

        self.assertEqual(name1[0], '28')

    def test_schedule1_overnight(self):
        name1, bus_schedule = schedule('3300', '2200', '3300', '2200', '', '', '', '', '', '294', '50000', '')

        self.assertEqual(name1[0], '28')
        self.assertEqual(name1[1], '6')
        self.assertEqual(name1[2], '6')

    def test_schedule2_day(self):
        name1, bus_schedule = schedule('3300', '2200', '3300', '2200', '', '', '', '', '', '294', '50000', '')

        self.assertEqual(name1[0], '28')
        self.assertEqual(name1[3], '1')
        self.assertEqual(name1[4], '1')

    def test_schedule3_plan(self):
        name1, bus_schedule = schedule('3300', '2200', '3300', '2200', '', '', '', '', '', '294', '50000', '')

        self.assertEqual(name1[0], '28')
        self.assertEqual(name1[1], '6')
        self.assertEqual(name1[2], '6')
        self.assertEqual(name1[3], '1')
        self.assertEqual(name1[4], '1')

    def test_schedule4_plan(self):
        name1, bus_schedule = schedule('3300', '2200', '3300', '2200', '', '', '', '', '', '394', '50000', '')

        self.assertEqual(name1[0], '28')
        self.assertEqual(name1[1], '7')
        self.assertEqual(name1[2], '7')
        self.assertEqual(name1[3], '1')
        self.assertEqual(name1[4], '1')


def main():
    unittest.main()


if __name__=='__main__':
    main()
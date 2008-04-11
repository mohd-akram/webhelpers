import re, string

class Time:
    
    def __init__(self):
        self.seconds=['s','sec','seconds','seconds']
        self.minutes=['min','minute','mins','minutes']
        self.hours=['hr','hours','hour']
        self.days=['day','days','d']
        self.weeks=['w','week','weeks']
        self.months=['month','months','mon']
        
    def getSeconds(self, parameter):
        if parameter in self.seconds:   return 1
        elif parameter in self.minutes: return 60
        elif parameter in self.hours:   return 60 * 60
        elif parameter in self.days:    return 60 * 60 * 24
        elif parameter in self.weeks:   return 60 * 60 * 24 * 7
        elif parameter in self.months:  return 60 * 60 * 24 * 30
        else: return 0
    
    def convertIntoSeconds(self, age):
        if age == None or age == '': return 0
        if re.match('\d+$', age): return int(age)
        match = re.match('(\d+)(' + string.join(self.seconds + self.minutes + self.hours + self.days + self.weeks + self.months, '|') + ')$', age)
        if match != None:
            number = int(match.group(1))
            return number * self.getSeconds(match.group(2))
        return -1
        
def seconds(value):
    t = Time()
    v = t.convertIntoSeconds(str(value))
    if v == -1:
        raise Exception('Invalid time, %s'%repr(value))
    return v
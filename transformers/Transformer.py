##
##

class Transformer(object):
    def __init__(self):
        self.name = "Transformer"

    def transform(self, frame):
        pass

class EMATransformer(Transformer):
    def __init__(self, emaName=None, sourceColumn="Close", periods=5):
        self.name = "EMATransformer"
        self.emaName = emaName
        self.sourceColumn = sourceColumn
        self.periods = periods
        

    def transform(self, frame):
        if self.emaName == None:
            self.emaName = "{0}_EMA_{1}".format(self.sourceColumn, self.periods)
        
        multiplier = 2.0/(self.periods + 1)
        frame[self.emaName] = frame[self.sourceColumn]

        for i in range(1, len(frame[self.sourceColumn])):
            prev_ema = frame[self.emaName][i - 1]
            curr_val = frame[self.sourceColumn][i]
            frame[self.emaName][i] = (curr_val - prev_ema) * multiplier + prev_ema
        return self.emaName

class MACDTransformer(Transformer):
    def __init__(self):
        self.name = "MACDTransformer"
        self.slow = 26
        self.slowColumn = None
        self.fast = 12
        self.fastColumn = None
        self.periods = 9
        self.macdName = "MACD"
        self.histName = "Histogram"
        self.signalName = "Signal"

    def transform(self, frame):
        if self.slowColumn == None:
            self.slowColumn = "Close_EMA_26"
        if self.fastColumn == None:
            self.fastColumn = "Close_EMA_12"

        if not self.slowColumn in frame.columns:
            xformer = EMATransformer(self.slowColumn, "Close", self.slow)
            xformer.transform(frame)

        if not self.fastColumn in frame.columns:
            xformer = EMATransformer(self.fastColumn, "Close", self.fast)
            xformer.transform(frame)

        frame[self.macdName] = frame[self.fastColumn] - frame[self.slowColumn]
        xformer = EMATransformer(self.signalName, self.macdName, self.periods)
        xformer.transform(frame)

        frame[self.histName] = frame[self.macdName] - frame[self.signalName]


class HighLowTransformer(Transformer):
    def __init__(self, highlowcol="HighLow", highvlaue="High", lowvalue="Low", lookback=5, lookforward=5):
        self.highLowColumn = "HighLow"
        self.highValue = "High"
        self.lowValue = "Low"
        self.lookBackward = lookback
        self.lookForward = lookforward

    def transform(self, frame):
        windowWidth = self.lookBackward + self.lookForward + 1
        frame[self.highLowColumn] = ""

        for i in range(windowWidth, len(frame)):
            subframe = frame[i - windowWidth:i]
            beforeFrame = subframe[0:self.lookBackward]
            afterFrame = subframe[-self.lookForward:]

            targetValue = subframe["High"][self.lookBackward]

            isHighest = True
            for j in range(len(beforeFrame)):
                if beforeFrame["High"][j] > targetValue:
                    isHighest = False
                    break

            for j in range(len(afterFrame)):
                if afterFrame["High"][j] > targetValue:
                    isHighest = False
                    break

            isLowest = False
            if not isHighest:
                targetValue = subframe["Low"][self.lookBackward]
                isLowest = True
                for j in range(len(beforeFrame)):
                    if beforeFrame["Low"][j] < targetValue:
                        isLowest = False
                        break
                for j in range(len(afterFrame)):
                    if afterFrame["Low"][j] < targetValue:
                        isLowest = False
                        break

            if isHighest:
                frame[self.highLowColumn][i - self.lookForward - 1] = self.highValue
            if isLowest:
                frame[self.highLowColumn][i - self.lookForward - 1] = self.lowValue


    

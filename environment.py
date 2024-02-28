import constants as const

class Environment () :
    def __init__ (self, address : int, neighbors : [int]) :
        self.address = address
        self.neighbors = [i for i in neighbors]
    
    @staticmethod
    def _format_neighbor_arr(arr : []) :
        ans = "["
        for el in arr : ans += f'"{const.DIRS_CONTAINER_NAME}{el}", '
        return ans[:-2] + "]"

    def format(self) :
        return {
            "address" : f"{const.DIRS_CONTAINER_NAME}{self.address}",
            "friends" : Environment._format_neighbor_arr(self.neighbors)
        }
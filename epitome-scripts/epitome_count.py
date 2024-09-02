import os
import re

def summary_ranges(nums):

        if len(nums) == 0:
            return ''

        ranges = []
        i = 0
        start_range = nums[0]

        while i < len(nums):
            if i == len(nums) - 1:
                if start_range == nums[i]:
                    ranges.append(f'{nums[i]}')
                else:
                    ranges.append(f'{start_range}->{nums[i]}')
                i += 1
            elif nums[i] == nums[i+1] - 1:
                i += 1
            else:
                if start_range == nums[i]:
                    ranges.append(f'{nums[i]}')
                else:
                    ranges.append(f'{start_range}->{nums[i]}')
                i += 1
                start_range = nums[i]

        return ranges

pattern = '\d+'

# selects the parent directory and then moves into the epitomes folder
path = os.path.join( os.path.dirname ( __file__), os.path.pardir, 'epitomes')

epitome_numbers = [int(re.search(pattern, file).group()) for file in os.listdir(path)]

print(f'{len(epitome_numbers)} have been transcribed. That is {len(epitome_numbers)/2191*100:.2f} percent of the 2191 total epitomes.')

print(summary_ranges(epitome_numbers))
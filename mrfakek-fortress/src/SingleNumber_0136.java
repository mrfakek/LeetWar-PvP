import java.util.Arrays;

public class SingleNumber_0136 {

    public int singleNumber(int[] nums) {
        Arrays.sort(nums);
        int arrSize = nums.length;
        for (int i = 0; i < arrSize - 1; i = i + 2) {
            int currentNum = nums[i];
            if (currentNum != nums[i + 1]) {
                return currentNum;
            }
        }
        return nums[arrSize - 1];
    }
}

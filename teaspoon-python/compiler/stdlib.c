
Array b_less(Array a, Array b)
{
	return new_array(1, (float[]){a.get[0] < b.get[0]});
}

Array b_eq(Array a, Array b)
{
	return new_array(1, (float[]){a.get[0] == b.get[0]});
}

Array b_sum(Array arr)
{
  float res = 0;
  for (int i=0; i<arr.len; i++)
    res += arr.get[i];
	return new_array(1, (float[]){res});
}

Array b_mul(Array arr)
{
  float res = 1;
  for (int i=0; i<arr.len; i++)
    res *= arr.get[i];
	return new_array(1, (float[]){res});
}

Array b_div(Array arr)
{
  float res = arr.get[0];
  for (int i=1; i<arr.len; i++)
    res /= arr.get[i];
	return new_array(1, (float[]){res});
}

Array b_push(Array* arr, Array v)
{
	// Right now, this is quite inefficient for code that makes heavy use of `push`, because Array is not equipped with a `size` attribute

	float f_arr[arr->len+v.len];
	Array new_arr = new_array(arr->len+v.len, f_arr);
	for (int i=0; i<arr->len; i++)
		new_arr.get[i] = arr->get[i];
	for (int i=0; i<v.len; i++)
		new_arr.get[arr->len+i] = v.get[i];

	arr = &new_arr;

	return new_array(0, (float[]){});
}

Array b_get(Array arr, Array i)
{
	return new_array(1, (float[]){arr.get[(int)i.get[0]]});
}

Array b_len(Array arr)
{
	return new_array(1, (float[]){arr.len});
}
var teaspoon_ex_while = `

main :
	x = 0

	while less x 5
		print "fabulous!\n"
		x = sum [x 1]
	end while

end function`

var teaspoon_ex_simple = `
hello y :
	x = [5,6,7,8]
	y = [8,6,7,8]
	z = [99,6,7,8]
	ret "Nice!\n"
end function

world :
	x = [5,6,7,8]
	y = [8,6,7,8]
	z = [99,6,7,8]
	ret x
end function

main :
	r = [7,7,7,7]
	x = 0
	while less x 5
		print (hello r)
		print mul sum 1 2 3
		x = sum x 1
	end while
end function`

var teaspoon_ex_if = `

main :

x = 5

if eq x 5
print "cool!"
end if

if eq x 4
print "uh oh!"
end if

end function`

var teaspoon_ex_array = `
main :

x = []
push x 65
push x 66
print x
print "\n"

end function`


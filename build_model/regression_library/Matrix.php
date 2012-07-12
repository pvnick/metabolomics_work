<?php
/**
 * Copyright (c)  2011 Shankar Manamalkav <nshankar@ufl.edu>
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * Simple matrix manipulation library
 *
 * @author shankar<nshankar@ufl.edu>
 */
class Lib_Matrix
{

    //global vars
    protected $rows;
    protected $columns;
    protected $MainMatrix = array();

    /**
     * Matrix Constructor
     * 
     * Initialize the Matrix object. Throw an exception if jagged array is passed.
     *
     * @param array $matrix - The array
     */
    function __construct($matrix)
    {
        for ($i = 0; $i < count($matrix); $i++)
        {
            for ($j = 0; $j < count($matrix[$i]); $j++)
                $this->MainMatrix[$i][$j] = $matrix[$i][$j];
        }
        $this->rows = count($this->MainMatrix);
        $this->columns = count($this->MainMatrix[0]);
        if (!$this->isValidMatrix())
        {
            throw new Exception("Invalid matrix");
        }
    }

    /**
     * Is it a valid matrix?
     * 
     * Returns 'False' if it is not a rectangular matrix
     *
     * @return bool
     */
    private function isValidMatrix()
    {
        for ($i = 0; $i < $this->rows; $i++)
        {
            $numCol = count($this->MainMatrix [$i]);
            if ($this->columns != $numCol)
                return false;
        }
        return true;
    }

    /**
     * Display the matrix
     * Formatted display of matrix for debugging.
     */
    public function DisplayMatrix()
    {
        $rows = $this->rows;
        $cols = $this->columns;
        echo "Order of the matrix is ($rows rows X $cols columns)\n";
        for ($r = 0; $r < $rows; $r++)
        {
            for ($c = 0; $c < $cols; $c++)
            {
                echo $this->MainMatrix[$r][$c];
            }
            echo "\n";
        }
    }

    /**
     * Get the inner array stored in matrix object
     * 
     * @return array 
     */
    public function GetInnerArray()
    {
        return $this->MainMatrix;
    }

    /**
     * Number of rows in the matrix
     * @return integer 
     */
    public function NumRows()
    {
        return count($this->MainMatrix);
    }

    /**
     * Number of columns in the matrix
     * @return integer
     */
    public function NumColumns()
    {
        return count($this->MainMatrix[0]);
    }

    /**
     * Return element found at location $row, $col.
     * 
     * @param int $row
     * @param int $col
     * @return object(depends on input)
     */
    public function GetElementAt($row, $col)
    {
        return $this->MainMatrix[$row][$col];
    }

    /**
     * Is this a square matrix?
     * 
     * Determinants and inverses only exist for square matrices!
     * 
     * @return bool 
     */
    public function isSquareMatrix()
    {
        if ($this->rows == $this->columns)
            return true;

        return false;
    }

    /**
     * Subtract matrix2 from matrix object on which this method is called
     * @param Lib_Matrix $matrix2
     * @return Lib_Matrix Note that original matrix is left unchanged
     */
    public function Subtract(Lib_Matrix $matrix2)
    {
        $rows1 = $this->rows;
        $columns1 = $this->columns;

        $rows2 = $matrix2->NumRows();
        $columns2 = $matrix2->NumColumns();

        if (($rows1 != $rows2) || ($columns1 != $columns2))
            throw new Exception('Matrices are not the same size!');

        for ($i = 0; $i < $rows1; $i++)
        {
            for ($j = 0; $j < $columns1; $j++)
            {
                $newMatrix[$i][$j] = $this->MainMatrix[$i][$j] -
                        $matrix2->GetElementAt($i, $j);
            }
        }
        return new Lib_Matrix($newMatrix);
    }

    /**
     * Add matrix2 to matrix object that calls this method.
     * @param Model_Matrix $matrix2
     * @return Lib_Matrix Note that original matrix is left unchanged
     */
    function Add(Lib_Matrix $matrix2)
    {
        $rows1 = $this->rows;
        $rows2 = $matrix2->NumRows();
        $columns1 = $this->columns;
        $columns2 = $matrix2->NumColumns();
        if (($rows1 != $rows2) || ($columns1 != $columns2))
            throw new Exception('Matrices are not the same size!');

        for ($i = 0; $i < $rows1; $i++)
        {
            for ($j = 0; $j < $columns1; $j++)
            {
                $newMatrix[$i][$j] = $this->MainMatrix[$i][$j] +
                        $matrix2->GetElementAt($i, $j);
            }
        }
        return new Lib_Matrix($newMatrix);
    }

    /**
     * Multiply matrix2 into matrix object that calls this method
     * @param Model_Matrix $matrix2
     * @return Lib_Matrix Note that original matrix is left unaltered
     */
    function Multiply(Lib_Matrix $matrix2)
    {
        $sum = 0;
        $rows1 = $this->rows;
        $columns1 = $this->columns;

        $columns2 = $matrix2->NumColumns();
        $rows2 = $matrix2->NumRows();
        if ($columns1 != $rows2)
            throw new Exception('Incompatible matrix types supplied');
        for ($i = 0; $i < $rows1; $i++)
        {
            for ($j = 0; $j < $columns2; $j++)
            {
                $newMatrix[$i][$j] = 0;
                for ($ctr = 0; $ctr < $columns1; $ctr++)
                {
                    $newMatrix[$i][$j] += $this->MainMatrix[$i][$ctr] *
                            $matrix2->GetElementAt($ctr, $j);
                }
            }
        }
        return new Lib_Matrix($newMatrix);
    }

    /**
     * Multiply every element of matrix on which this method is called by the scalar
     * @param object $scalar
     * @return Lib_Matrix 
     */
    public function ScalarMultiply($scalar)
    {
        $rows = $this->rows;
        $columns = $this->columns;

        $newMatrix = array();
        for ($i = 0; $i < $rows; $i++)
        {
            for ($j = 0; $j < $columns; $j++)
            {
                $newMatrix[$i][$j] = $this->MainMatrix[$i][$j] * $scalar;
            }
        }
        return new Lib_Matrix($newMatrix);
    }

    /**
     * Divide every element of matrix on which this method is called by the scalar
     * @param object $scalar
     * @return Lib_Matrix 
     */
    public function ScalarDivide($scalar)
    {
        $rows = $this->rows;
        $columns = $this->columns;

        $newMatrix = array();
        for ($i = 0; $i < $rows; $i++)
        {
            for ($j = 0; $j < $columns; $j++)
            {
                if ($scalar == 0) {
                    throw new Exception('about to divide by zero, disregard this result.');
                }
                $newMatrix[$i][$j] = $this->MainMatrix[$i][$j] / $scalar;
            }
        }
        return new Lib_Matrix($newMatrix);
    }

    /**
     * Return the sub-matrix after crossing out the $crossx and $crossy row and column respectively
     * Part of determinant expansion by minors method
     * @param int $crossX
     * @param int $crossY
     * @return Lib_Matrix 
     */
    public function GetSubMatrix($crossX, $crossY)
    {
        $rows = $this->rows;
        $columns = $this->columns;

        $newMatrix = array();
        $p = 0; // submatrix row counter
        for ($i = 0; $i < $rows; $i++)
        {
            $q = 0; // submatrix col counter
            if ($crossX != $i)
            {
                for ($j = 0; $j < $columns; $j++)
                {
                    if ($crossY != $j)
                    {
                        $newMatrix[$p][$q] = $this->GetElementAt($i, $j);
                        //$matrix[$i][$j];
                        $q++;
                    }
                }
                $p++;
            }
        }
        return new Lib_Matrix($newMatrix);
    }

    /**
     * Compute the determinant of the square matrix on which this method is called
     * @link http://mathworld.wolfram.com/DeterminantExpansionbyMinors.html
     * @return object(depends on input)
     */
    public function Determinant()
    {
        if (!$this->isSquareMatrix())
            throw new Exception("Not a square matrix!");
        $rows = $this->rows;
        $columns = $this->columns;
        $determinant = 0;
        if ($rows == 1 && $columns == 1)
        {
            return $this->MainMatrix[0][0];
        }
        if ($rows == 2 && $columns == 2)
        {
            $determinant = $this->MainMatrix[0][0] * $this->MainMatrix[1][1] -
                    $this->MainMatrix[0][1] * $this->MainMatrix[1][0];
        } else
        {
            for ($j = 0; $j < $columns; $j++)
            {
                $subMatrix = $this->GetSubMatrix(0, $j);
                if (fmod($j, 2) == 0)
                {
                    $determinant += $this->MainMatrix[0][$j] * $subMatrix->Determinant();
                } else
                {
                    $determinant -= $this->MainMatrix[0][$j] * $subMatrix->Determinant();
                }
            }
        }
        return $determinant;
    }

    /**
     * Compute the transpose of matrix on which this method is called (invert rows and columns)
     * @return Lib_Matrix 
     */
    public function Transpose()
    {
        $rows = $this->rows;
        $columns = $this->columns;
        $newArray = array();
        for ($i = 0; $i < $rows; $i++)
        {
            for ($j = 0; $j < $columns; $j++)
            {
                $newArray[$j][$i] = $this->MainMatrix[$i][$j];
            }
        }
        return new Lib_Matrix($newArray);
    }

    /**
     * Compute the inverse of the matrix on which this method is found (A*A(-1)=I)
     * (cofactor(a))T/(det a)
     * @link http://www.mathwords.com/i/inverse_of_a_matrix.htm
     * @return Lib_Matrix 
     */
    function Inverse()
    {
        if (!$this->isSquareMatrix())
            throw new Exception("Not a square matrix!");
        $rows = $this->rows;
        $columns = $this->columns;

        $newMatrix = array();
        for ($i = 0; $i < $rows; $i++)
        {
            for ($j = 0; $j < $columns; $j++)
            {
                $subMatrix = $this->GetSubMatrix($i, $j);
                if (fmod($i + $j, 2) == 0)
                {
                    $newMatrix[$i][$j] = ($subMatrix->Determinant());
                } else
                {
                    $newMatrix[$i][$j] = -($subMatrix->Determinant());
                }
            }
        }
        $cofactorMatrix = new Lib_Matrix($newMatrix);
        return $cofactorMatrix->Transpose()
                ->ScalarDivide($this->Determinant());
    }
}

?>

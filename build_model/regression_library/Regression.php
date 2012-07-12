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
 * Class for computing multiple linear regression of the form
 * y=a+b1x1+b2x2+b3x3...
 *
 * @author shankar<nshankar@ufl.edu>
 * 
 * 
 */
class Lib_Regression
{

    protected $SSEScalar; //sum of squares due to error
    protected $SSRScalar; //sum of squares due to regression
    protected $SSTOScalar; //Total sum of squares
    protected $RSquare;         //R square
    protected $RSquarePValue;   //R square p falue (significant f)
    protected $F;               //F statistic
    protected $coefficients;    //regression coefficients array
    protected $stderrors;    //standard errror array
    protected $tstats;     //t statistics array
    protected $pvalues;     //p values array
    protected $x = array();
    protected $y = array();

    //implement singleton
    /**
     * An instance of this class (singleton)
     * @var Lib_Regression 
     */
    public function setX($x)
    {
        $this->x = $x;
    }

    public function setY($y)
    {
        $this->y = $y;
    }

    public function getSSE()
    {
        return $this->SSEScalar;
    }

    public function getSSR()
    {
        return $this->SSRScalar;
    }

    public function getSSTO()
    {
        return $this->SSTOScalar;
    }

    public function getRSQUARE()
    {
        return $this->RSquare;
    }
    public function getRSQUAREPValue()
    {
        return $this->RSquarePValue;
    }

    public function getF()
    {
        return $this->F;
    }

    public function getCoefficients()
    {
        return $this->coefficients;
    }

    public function getStandardError()
    {
        return $this->stderrors;
    }

    public function getTStats()
    {
        return $this->tstats;
    }

    public function getPValues()
    {
        return $this->pvalues;
    }

    /**
     * @example $reg->loadCSV('abc.csv',array(0), array(1,2,3));
     * @param type $file
     * @param array $xcolnumbers
     * @param type $ycolnumber 
     */
    public function LoadCSV($file, array $ycol, array $xcol, $hasHeader=true)
    {
        $xarray = array();
        $yarray = array();
        $handle = fopen($file, "r");

        //if first row has headers.. ignore
        if ($hasHeader)
            $data = fgetcsv($handle);
        //get the data into array
        while (($data = fgetcsv($handle)) !== FALSE)
        {
            $rawData[] = array($data);
        }
        $sampleSize = count($rawData);

        $r = 0;
        while ($r < $sampleSize)
        {
            $xarray[] = $this->GetArray($rawData, $xcol, $r, true);
            $yarray[] = $this->GetArray($rawData, $ycol, $r);   //y always has 1 col!
            $r++;
        }
        $this->x = $xarray;
        $this->y = $yarray;
    }

    private function GetArray($rawData, $cols, $r, $incIntercept=false)
    {
        $arrIdx = "";
        $z = 0;
        $arr = array();
        if ($incIntercept)
            //prepend an all 1's column for the intercept
            $arr[]=1;
        foreach ($cols as $key => $val)
        {
            $arrIdx = '$rawData[' . $r . '][0][' . $val . '];';
			$z = $rawData[$r][0][$val];
            //eval("\$z = $arrIdx");
            $arr[] = $z;
        }
        return $arr;
    }
    //if true is passed to this method, compute normalized coefficients
    public function Compute($computeNormalized=false)
    {
        if ((count($this->x)==0)||(count($this->y)==0))
                throw new Exception ('Please supply valid X and Y arrays');
        $mx = new Lib_Matrix($this->x);
        $my = new Lib_Matrix($this->y);

        //coefficient(b) = (X'X)-1X'Y 
        $xTx = $mx->Transpose()->Multiply($mx)->Inverse();
        $xTy = $mx->Transpose()->Multiply($my);

        $coeff = $xTx->Multiply($xTy);

        $num_independent = $mx->NumColumns();   //note: intercept is included
        $sample_size = $mx->NumRows();
        $dfTotal = $sample_size - 1;
        $dfModel = $num_independent - 1;
        $dfResidual = $dfTotal - $dfModel;
        //create unit vector..
        for ($ctr = 0; $ctr < $sample_size; $ctr++)
            $u[] = array(1);

        $um = new Lib_Matrix($u);
        //SSR = b(t)X(t)Y - (Y(t)UU(T)Y)/n        
        //MSE = SSE/(df)
        $SSR = $coeff->Transpose()->Multiply($mx->Transpose())->Multiply($my)
                ->Subtract(
                        ($my->Transpose()
                        ->Multiply($um)
                        ->Multiply($um->Transpose())
                        ->Multiply($my)
                        ->ScalarDivide($sample_size))
        );

        $SSE = $my->Transpose()->Multiply($my)->Subtract(
                        $coeff->Transpose()
                                ->Multiply($mx->Transpose())
                                ->Multiply($my)
        );

        $SSTO = $SSR->Add($SSE);
        $this->SSEScalar = $SSE->GetElementAt(0, 0);
        $this->SSRScalar = $SSR->GetElementAt(0, 0);
        $this->SSTOScalar = $SSTO->GetElementAt(0, 0);

        $this->RSquare = $this->SSRScalar / $this->SSTOScalar;


        $this->F = (($this->SSRScalar / ($dfModel)) / ($this->SSEScalar / ($dfResidual)));
	
	$this->RSquarePValue= $this->FishersF($this->F, $dfModel, $dfResidual);
	
        $MSE = $SSE->ScalarDivide($dfResidual);
        //this is a scalar.. get element
        $e = ($MSE->GetElementAt(0, 0));

        $stdErr = $xTx->ScalarMultiply($e);
        for ($i = 0; $i < $num_independent; $i++)
        {
            //get the diagonal elements
            $searray[] = array(sqrt($stdErr->GetElementAt($i, $i)));
            //compute the t-statistic
            if ($searray[$i][0] == 0) {
                throw new Exception('about to divide by zero, disregard this result.');
            }
            $tstat[] = array($coeff->GetElementAt($i, 0) / $searray[$i][0]);
            //compute the student p-value from the t-stat
            $pvalue[] = array($this->Student_PValue($tstat[$i][0], $dfResidual));
        }
        //convert into 1-d vectors and store
        for ($ctr = 0; $ctr < $num_independent; $ctr++)
        {
            $this->coefficients[] = $coeff->GetElementAt($ctr, 0);
            $this->stderrors[] = $searray[$ctr][0];
            $this->tstats[] = $tstat[$ctr][0];
            $this->pvalues[] = $pvalue[$ctr][0];
        }
	/* multiplying the unstandardized coefficient by the ratio of the standard deviations 
         * of the independent variable (x) and dependent variable(y) gives us NORMALIZED coefft.
         */
        if ($computeNormalized)
        {
            //if normalized betas are desired, compute them
            $this->coefficients = $this->ComputeNormalizedBeta($this->coefficients, 
                    $mx->GetInnerArray(), $my->GetInnerArray());
        }
    }

    
    private function ComputeNormalizedBeta($beta, $x, $y)
    {
        $betaNormalized=array();
        $cols = count($x[0]);
        for ($i = 1; $i < $cols; $i++)
        {
            ${'xvar' . $i} = $this->ComputeStdev($x, $i);
        }
        $yvar1 = $this->ComputeStdev($y, 0);
        $betaNormalized[0] = 0;  //Normalized coeff. intercept is not defined
        for ($i = 1; $i < count($beta); $i++)
        {
            $betaNormalized[] = $beta[$i] * ${'xvar' . $i} / $yvar1;
        }
        return $betaNormalized;
    }

    private function ComputeStdev($arr, $column)
    {
        //$arr is a 2d matrix
        //compute stdev of a particular column of a 2d array
        //standardized x and y.
        $rows = count($arr);
        
        for ($i = 0; $i < $rows; $i++)
        {
            $x[] = $arr[$i][$column];
        }
        $stDevX = $this->StdDeviation($x);
        return $stDevX;
    }

    //compute the standard deviation of 1-d array that is passed in
    private function StdDeviation($sample)
    {
        //compute mean
        $mean = array_sum($sample) / sizeof($sample);
        //loop through all and find square of difference betn each and mean
        foreach ($sample as $num)
        {
            $devs[] = pow(($num - $mean), 2);
        }
        //finally, take square root of average of those..
        $std = sqrt(array_sum($devs) / count($devs));
        return $std;
    }
    /**
     * @link http://home.ubalt.edu/ntsbarsh/Business-stat/otherapplets/pvalues.htm#rtdist
     * @param float $t_stat
     * @param float $deg_F
     * @return float 
     */
    private function Student_PValue($t_stat, $deg_F)
    {
        $t_stat = abs($t_stat);
        $mw = $t_stat / sqrt($deg_F);
        $th = atan2($mw, 1);
        if ($deg_F == 1)
            return 1.0 - $th / (M_PI / 2.0);
        $sth = sin($th);
        $cth = cos($th);
        if ($deg_F % 2 == 1)
            return 1.0 - ($th + $sth * $cth * $this->statcom($cth * $cth, 2, $deg_F - 3, -1)) / (M_PI / 2.0);
        else
            return 1.0 - ($sth * $this->statcom($cth * $cth, 1, $deg_F - 3, -1));
    }

    /**
     * @link http://home.ubalt.edu/ntsbarsh/Business-stat/otherapplets/pvalues.htm#rtdist
     * @param float $q
     * @param float $i
     * @param float $j
     * @param float $b
     * @return float 
     */
    private function statcom($q, $i, $j, $b)
    {
        $zz = 1;
        $z = $zz;
        $k = $i;
        while ($k <= $j)
        {
            $zz = $zz * $q * $k / ( $k - $b);
            $z = $z + $zz;
            $k = $k + 2;
        }
        return $z;
    }
    /**
     *Formula to return Fishers F (P Value of RSquare) (Significance F)
     * @param type $f - F statistic computed from regression analysis
     * @param float $n1 - Degrees of freedom1 (regression)
     * @param int $n2 - Degrees of freedom2 (residual)
     * @return float 
     */
    private function  FishersF($f,$n1, $n2)
    {
        $x = $n2/($n1*$f+$n2);
        if ($n1 % 2 == 0)
            return ($this->statcom(1-$x,$n2,$n1+$n2-4,$n2-2)*pow($x,$n2/2));
        if ($n2 % 2 == 0)
            return (1 - $this->statcom($x,$n1,$n1+$n2-4,$n1-2)*pow(1-$x,$n1/2));
        $th = atan(sqrt($n1*$f/$n2));
        $a = $th/(M_PI / 2.0);
        $sth = sin($th);
        $cth = cos($th);
        if ($n2>1)
            $a+=$sth*$cth*($this->statcom($cth*$cth, 2, $n2-3, -1)/(M_PI / 2.0));
        if ($n1==1)
            return 1-$a;
        $c = 4*$this->statcom($sth*$sth, $n2+1, $n1+$n2-4, $n2-2)*$sth*pow($cth,$n2)/M_PI;
        if ($n2==1)
            return (1-$a+$c/2);
        $k=2;
        while ($k<=($n2-1)/2)
        {
            $c = $c*$k/($k-.5);
            $k++;
        }
        return (1-$a+$c);
    }

}

?>
